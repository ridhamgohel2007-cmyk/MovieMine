"""
MovieMine Data Mining Layer: Association Rule Mining (Apriori Algorithm)
Academic Topic: Market Basket Analysis & Frequent Pattern Mining

========================================================================
ACADEMIC FLOW:
INPUT          : Transaction Database T where each transaction is a user's collection
                 of highly rated (rating >= 3.5) or watched movies.
PREPROCESSING  : 
                 1. Build user transaction lists: { User_i: [Movie_A, Movie_B, Movie_C] }
                 2. Filter out trivial baskets (length < 2)
                 3. Encode into boolean incidence matrix using TransactionEncoder.
ALGORITHM      : 
                 1. Apriori Frequent Itemset Generation (mlxtend.frequent_patterns.apriori):
                    - Uses Apriori property / anti-monotonicity (downward closure):
                      "All non-empty subsets of a frequent itemset must also be frequent."
                    - Prunes itemsets with Support < min_support.
                 2. Association Rule Derivation (mlxtend.frequent_patterns.association_rules):
                    - Rule A -> B
                    - Support(A -> B) = P(A ∩ B) = Count(A ∩ B) / Total_Transactions
                    - Confidence(A -> B) = P(B | A) = Support(A ∩ B) / Support(A)
                    - Lift(A -> B) = Confidence(A -> B) / Support(B)
OUTPUT         : Mined association rules sorted by Lift / Confidence.
INTERPRETATION : Lift > 1 denotes positive correlation; higher lift indicates stronger
                 dependency between watching Antecedent and Consequent.
========================================================================
"""

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from sqlalchemy.orm import Session
from models.models import Rating, WatchHistory, Movie, AssociationRuleModel

class AssociationRuleMiner:
    def __init__(self, db: Session):
        self.db = db

    def extract_transactions(self) -> tuple[list[list[str]], dict]:
        """
        Creates transactions from user watch history and positive ratings (>= 3.5).
        Returns list of transactions (list of movie titles) and user-to-basket mapping.
        """
        # Fetch positive ratings
        ratings = self.db.query(Rating.user_id, Movie.title).join(Movie).filter(Rating.rating >= 3.5).all()
        # Fetch watch history
        history = self.db.query(WatchHistory.user_id, Movie.title).join(Movie).all()

        user_baskets = {}
        for uid, title in ratings + history:
            if uid not in user_baskets:
                user_baskets[uid] = set()
            user_baskets[uid].add(title)

        # Retain only transactions with at least 2 distinct items
        valid_transactions = [list(basket) for basket in user_baskets.values() if len(basket) >= 2]
        return valid_transactions, user_baskets

    def mine_rules(
        self,
        min_support: float = 0.08,
        min_confidence: float = 0.40,
        min_lift: float = 1.0,
        max_rules: int = 50
    ) -> dict:
        """
        Executes Apriori frequent itemset generation and derives association rules.
        Persists top mined rules to the 'association_rules' database table.
        """
        transactions, user_baskets = self.extract_transactions()

        if not transactions or len(transactions) < 5:
            return {
                "success": False,
                "message": f"Insufficient user transactions ({len(transactions)}) to mine association rules. Need more ratings/views.",
                "rules": []
            }

        # 1. Encode transactions into boolean matrix
        te = TransactionEncoder()
        te_ary = te.fit(transactions).transform(transactions)
        df_encoded = pd.DataFrame(te_ary, columns=te.columns_)

        # 2. Frequent Itemset Generation using Apriori
        try:
            frequent_itemsets = apriori(
                df_encoded,
                min_support=min_support,
                use_colnames=True,
                max_len=3
            )
        except Exception as e:
            return {
                "success": False,
                "message": f"Apriori execution failed: {str(e)}",
                "rules": []
            }

        if frequent_itemsets.empty:
            # Fallback attempt with slightly lower support if user set it too high
            fallback_sup = max(0.04, min_support / 2)
            frequent_itemsets = apriori(df_encoded, min_support=fallback_sup, use_colnames=True, max_len=3)
            if frequent_itemsets.empty:
                return {
                    "success": True,
                    "message": f"No itemsets met min_support={min_support}. Try lowering support threshold.",
                    "total_transactions": len(transactions),
                    "frequent_itemsets_count": 0,
                    "rules": []
                }

        # 3. Association Rule Generation
        try:
            rules_df = association_rules(
                frequent_itemsets,
                metric="confidence",
                min_threshold=min_confidence
            )
        except Exception as e:
            return {
                "success": False,
                "message": f"Rule derivation failed: {str(e)}",
                "rules": []
            }

        if rules_df.empty:
            return {
                "success": True,
                "message": f"No rules met min_confidence={min_confidence}. Try lowering confidence threshold.",
                "total_transactions": len(transactions),
                "frequent_itemsets_count": len(frequent_itemsets),
                "rules": []
            }

        # Filter by min_lift and sort by lift descending
        rules_df = rules_df[rules_df["lift"] >= min_lift]
        rules_df = rules_df.sort_values(by=["lift", "confidence"], ascending=[False, False]).head(max_rules)

        # 4. Clear and persist top rules in database
        self.db.query(AssociationRuleModel).delete()
        self.db.commit()

        results = []
        for _, row in rules_df.iterrows():
            antecedent_str = ", ".join(list(row["antecedents"]))
            consequent_str = ", ".join(list(row["consequents"]))
            sup = round(float(row["support"]), 4)
            conf = round(float(row["confidence"]), 4)
            lift = round(float(row["lift"]), 4)

            # Persist
            rule_entry = AssociationRuleModel(
                antecedent=antecedent_str,
                consequent=consequent_str,
                support=sup,
                confidence=conf,
                lift=lift
            )
            self.db.add(rule_entry)

            # Academic interpretation string
            explanation = (
                f"Users who liked [{antecedent_str}] have a {int(conf*100)}% likelihood "
                f"of also liking [{consequent_str}] ({lift:.2f}x higher than baseline rate)."
            )

            results.append({
                "rule_id": len(results) + 1,
                "antecedent": antecedent_str,
                "consequent": consequent_str,
                "support": sup,
                "confidence": conf,
                "lift": lift,
                "explanation": explanation
            })

        self.db.commit()

        return {
            "success": True,
            "total_transactions": len(transactions),
            "frequent_itemsets_count": len(frequent_itemsets),
            "rules_count": len(results),
            "rules": results
        }

    def get_existing_rules(self) -> list:
        """
        Retrieves already mined rules from the database.
        """
        rules = self.db.query(AssociationRuleModel).order_by(AssociationRuleModel.lift.desc()).all()
        return [r.to_dict() for r in rules]

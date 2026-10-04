import React, { useState } from 'react';
import { UserProvider } from './context/UserContext';
import Navbar from './components/Navbar';
import RatingModal from './components/RatingModal';

// Simplified, clean 4 pages
import Recommendations from './pages/Recommendations';
import ClusterAnalysis from './pages/ClusterAnalysis';
import AssociationRules from './pages/AssociationRules';
import SystemInfo from './pages/SystemInfo';
import MovieDetail from './pages/MovieDetail';

function AppContent() {
  const [activeTab, setActiveTab] = useState('recommendations');
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [ratingMovie, setRatingMovie] = useState(null);
  const [isRatingModalOpen, setIsRatingModalOpen] = useState(false);

  const handleSelectMovie = (movie) => {
    setSelectedMovie(movie);
  };

  const handleOpenRatingModal = (movie) => {
    setRatingMovie(movie);
    setIsRatingModalOpen(true);
  };

  const handleCloseRatingModal = () => {
    setIsRatingModalOpen(false);
    setRatingMovie(null);
  };

  const renderActivePage = () => {
    if (selectedMovie) {
      return (
        <MovieDetail
          movie={selectedMovie}
          onBack={() => setSelectedMovie(null)}
          onSelectMovie={handleSelectMovie}
          onRateMovie={handleOpenRatingModal}
        />
      );
    }

    switch (activeTab) {
      case 'recommendations':
        return (
          <Recommendations
            onSelectMovie={handleSelectMovie}
            onRateMovie={handleOpenRatingModal}
          />
        );
      case 'clusters':
        return <ClusterAnalysis />;
      case 'rules':
        return <AssociationRules />;
      case 'viva':
        return <SystemInfo />;
      default:
        return (
          <Recommendations
            onSelectMovie={handleSelectMovie}
            onRateMovie={handleOpenRatingModal}
          />
        );
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
      {/* Top Navbar */}
      <Navbar
        activeTab={selectedMovie ? 'recommendations' : activeTab}
        setActiveTab={(tab) => {
          setSelectedMovie(null);
          setActiveTab(tab);
        }}
      />

      {/* Main Content Viewport */}
      <main className="flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 pt-6">
        {renderActivePage()}
      </main>

      {/* Global Interactive Star Rating Modal */}
      <RatingModal
        movie={ratingMovie}
        isOpen={isRatingModalOpen}
        onClose={handleCloseRatingModal}
        onRatingSubmitted={() => {}}
      />

      {/* Clean Modern Footer */}
      <footer className="border-t border-slate-800/80 bg-slate-950 py-6 text-center text-xs text-slate-400">
        <div className="max-w-6xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="font-bold text-white tracking-tight">MovieMine</span>
            <span className="text-[10px] text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20">
              Data Mining Academic Project
            </span>
          </div>
          <p className="text-slate-400">
            K-Means Clustering • Apriori Rules • Hybrid Recommendation (0.5 Collab + 0.3 Content + 0.2 Pop)
          </p>
          <div className="text-[11px] text-slate-400">
            College Viva Defense System
          </div>
        </div>
      </footer>
    </div>
  );
}

function App() {
  return (
    <UserProvider>
      <AppContent />
    </UserProvider>
  );
}

export default App;

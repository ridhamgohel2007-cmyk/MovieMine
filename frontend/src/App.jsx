import React, { useState } from 'react';
import { UserProvider } from './context/UserContext';
import Navbar from './components/Navbar';
import RatingModal from './components/RatingModal';

import BrowseAndRecs from './pages/BrowseAndRecs';
import ClusterAnalysis from './pages/ClusterAnalysis';
import AssociationRules from './pages/AssociationRules';
import MovieDetail from './pages/MovieDetail';

function AppContent() {
  const getInitialTab = () => {
    const params = new URLSearchParams(window.location.search);
    const tabParam = params.get('tab');
    if (tabParam) return tabParam;
    const hash = window.location.hash.replace('#', '');
    if (['browse', 'clusters', 'patterns'].includes(hash)) return hash;
    return 'browse';
  };

  const [activeTab, setActiveTab] = useState(getInitialTab);
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
      case 'browse':
        return (
          <BrowseAndRecs
            onSelectMovie={handleSelectMovie}
            onRateMovie={handleOpenRatingModal}
          />
        );
      case 'clusters':
        return <ClusterAnalysis />;
      case 'patterns':
        return <AssociationRules />;
      default:
        return (
          <BrowseAndRecs
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
        activeTab={selectedMovie ? 'browse' : activeTab}
        setActiveTab={(tab) => {
          setSelectedMovie(null);
          setActiveTab(tab);
        }}
      />

      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 pt-6">
        {renderActivePage()}
      </main>

      {/* Star Rating Modal */}
      <RatingModal
        movie={ratingMovie}
        isOpen={isRatingModalOpen}
        onClose={handleCloseRatingModal}
        onRatingSubmitted={() => {}}
      />

      {/* Simple Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="font-black text-white tracking-tight">MovieMine</span>
            <span className="text-[10px] text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20 font-bold">
              Data Mining System
            </span>
          </div>
          <p className="text-slate-400 text-xs">
            K-Means Clustering • Apriori Rule Mining • Collaborative & Content Recommendations
          </p>
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

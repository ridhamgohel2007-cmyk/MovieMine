import React, { useState } from 'react';
import { UserProvider } from './context/UserContext';
import Navbar from './components/Navbar';
import RatingModal from './components/RatingModal';

// Pages
import Home from './pages/Home';
import Movies from './pages/Movies';
import MovieDetail from './pages/MovieDetail';
import Recommendations from './pages/Recommendations';
import MyRatings from './pages/MyRatings';
import UserProfile from './pages/UserProfile';
import DataMiningDashboard from './pages/DataMiningDashboard';
import ClusterAnalysis from './pages/ClusterAnalysis';
import AssociationRules from './pages/AssociationRules';
import ClassificationDemo from './pages/ClassificationDemo';
import SystemInfo from './pages/SystemInfo';

function AppContent() {
  const [activeTab, setActiveTab] = useState('home');
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
    // If a movie is selected, show MovieDetail view regardless of tab, with back button
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
      case 'home':
        return (
          <Home
            onSelectMovie={handleSelectMovie}
            onRateMovie={handleOpenRatingModal}
            setActiveTab={setActiveTab}
          />
        );
      case 'movies':
        return (
          <Movies
            onSelectMovie={handleSelectMovie}
            onRateMovie={handleOpenRatingModal}
          />
        );
      case 'recommendations':
        return (
          <Recommendations
            onSelectMovie={handleSelectMovie}
            onRateMovie={handleOpenRatingModal}
          />
        );
      case 'ratings':
        return (
          <MyRatings
            onSelectMovie={handleSelectMovie}
            onRateMovie={handleOpenRatingModal}
            setActiveTab={setActiveTab}
          />
        );
      case 'dashboard':
        return <DataMiningDashboard setActiveTab={setActiveTab} />;
      case 'clusters':
        return <ClusterAnalysis />;
      case 'association':
        return <AssociationRules />;
      case 'classifier':
        return <ClassificationDemo />;
      case 'profile':
        return <UserProfile />;
      case 'viva':
        return <SystemInfo />;
      default:
        return (
          <Home
            onSelectMovie={handleSelectMovie}
            onRateMovie={handleOpenRatingModal}
            setActiveTab={setActiveTab}
          />
        );
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
      {/* Top Navbar */}
      <Navbar
        activeTab={selectedMovie ? 'movies' : activeTab}
        setActiveTab={(tab) => {
          setSelectedMovie(null);
          setActiveTab(tab);
        }}
      />

      {/* Main Content Viewport */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-6">
        {renderActivePage()}
      </main>

      {/* Global Interactive Star Rating Modal */}
      <RatingModal
        movie={ratingMovie}
        isOpen={isRatingModalOpen}
        onClose={handleCloseRatingModal}
        onRatingSubmitted={() => {
          // Trigger refresh if needed
        }}
      />

      {/* Academic Project Footer */}
      <footer className="border-t border-slate-800 bg-slate-900/60 py-8 text-center text-xs text-slate-400">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="font-bold text-white tracking-tight">MovieMine</span>
            <span className="text-[10px] text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20">
              Data Mining Academic Project
            </span>
          </div>
          <p className="text-slate-400">
            Powered by Flask, SQLAlchemy, Scikit-Learn, MLxtend, MySQL / SQLite & React
          </p>
          <div className="text-[11px] text-slate-400">
            Built for College Data Mining Subject Viva Demonstration
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

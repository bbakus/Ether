import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landing from './components/Landing';
import Home from './components/Home';
import Spread from './components/Spread';


function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/home" element={<Home />} />
          <Route path="/spread" element={<Spread />} />
          <Route path="/spread/:spreadType" element={<Spread />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

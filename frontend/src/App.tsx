import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router';
import { Home } from './pages/Home';
import { Dashboard, CreateActivity, DashboardHome } from './pages/dashboard/';
import { Activities } from './pages/dashboard/Activities';
import { Clients } from './pages/dashboard/Clients';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />}>
          <Route index element={<DashboardHome />} />
          <Route path="create-activity" element={<CreateActivity />} />
          <Route path="activities" element={<Activities />} />
          <Route path="clients" element={<Clients />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;

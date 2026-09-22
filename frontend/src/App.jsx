import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';

import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Employees from './pages/Employees';
import Recruitment from './pages/Recruitment';
import Attendance from './pages/Attendance';
import Payroll from './pages/Payroll';
import ProjectsTasks from './pages/ProjectsTasks';
import AIIntelligence from './pages/AIIntelligence';
import Quotations from './pages/Quotations';
import AuditLogs from './pages/AuditLogs';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />

          <Route element={<ProtectedRoute title="Executive Dashboard" />}>
            <Route path="/dashboard" element={<Dashboard />} />
          </Route>

          <Route element={<ProtectedRoute title="Employee Directory & Org Chart" />}>
            <Route path="/employees" element={<Employees />} />
          </Route>

          <Route element={<ProtectedRoute title="Talent Acquisition & Hiring Pipeline" />}>
            <Route path="/recruitment" element={<Recruitment />} />
          </Route>

          <Route element={<ProtectedRoute title="Time & Attendance Tracking" />}>
            <Route path="/attendance" element={<Attendance />} />
          </Route>

          <Route element={<ProtectedRoute title="Compensation & Payroll Hub" />}>
            <Route path="/payroll" element={<Payroll />} />
          </Route>

          <Route element={<ProtectedRoute title="Engineering Sprint & Kanban Board" />}>
            <Route path="/projects" element={<ProjectsTasks />} />
          </Route>

          <Route element={<ProtectedRoute title="AI Skill Gap & Learning Portal" />}>
            <Route path="/ai-intelligence" element={<AIIntelligence />} />
          </Route>

          <Route element={<ProtectedRoute title="Quotation & Product Builder" />}>
            <Route path="/quotations" element={<Quotations />} />
          </Route>

          <Route element={<ProtectedRoute allowedRoles={['SUPER_ADMIN', 'HR_ADMIN']} title="Security Audit Logs" />}>
            <Route path="/audit-logs" element={<AuditLogs />} />
          </Route>

          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;

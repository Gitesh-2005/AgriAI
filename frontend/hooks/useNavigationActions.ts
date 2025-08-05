import { useCallback } from 'react';
import { useNavigate } from 'react-router-dom';

export const useNavigationActions = () => {
  const navigate = useNavigate();

  const goToDashboard = useCallback(() => {
    navigate('/dashboard');
  }, [navigate]);

  const goToHome = useCallback(() => {
    navigate('/');
  }, [navigate]);

  return {
    goToDashboard,
    goToHome
  };
};
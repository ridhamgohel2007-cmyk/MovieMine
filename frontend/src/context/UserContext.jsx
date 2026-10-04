import React, { createContext, useContext, useState, useEffect } from 'react';
import { userApi } from '../services/api';

const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [users, setUsers] = useState([]);
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      const res = await userApi.getUsers();
      const userList = res.data || [];
      setUsers(userList);

      const savedUserId = localStorage.getItem('moviemine_user_id');
      if (savedUserId) {
        const found = userList.find((u) => u.user_id === parseInt(savedUserId, 10));
        if (found) {
          setCurrentUser(found);
          setLoading(false);
          return;
        }
      }

      if (userList.length > 0) {
        setCurrentUser(userList[0]);
        localStorage.setItem('moviemine_user_id', userList[0].user_id);
      }
    } catch (err) {
      console.error('Failed to load users:', err);
    } finally {
      setLoading(false);
    }
  };

  const switchUser = (user) => {
    setCurrentUser(user);
    localStorage.setItem('moviemine_user_id', user.user_id);
  };

  return (
    <UserContext.Provider value={{ users, currentUser, switchUser, loading, refreshUsers: loadUsers }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => useContext(UserContext);

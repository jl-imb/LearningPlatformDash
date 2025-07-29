import React, { useEffect, useState } from 'react';
import { getProfile, getModules, completeLesson, getUserProgress, getRecentActivities } from '../services/api';
import './Dashboard.css';

function Dashboard() {
  const [profile, setProfile] = useState(null);
  const [modules, setModules] = useState([]);
  const [userProgress, setUserProgress] = useState([]);
  const [recentActivities, setRecentActivities] = useState([]);

  useEffect(() => {
    async function load() {
      try {
        const user = await getProfile();
        const mods = await getModules();
        const progress = await getUserProgress(user.email);
        const activities = await getRecentActivities();
        
        setProfile(user);
        setModules(mods);
        setUserProgress(progress);
        setRecentActivities(activities);
      } catch (err) {
        console.error('Error loading dashboard:', err);
        alert("Session expired. Please log in again.");
        localStorage.removeItem("token");
        window.location.href = "/login";
      }
    }
    load();
  }, []);

  const handleCompleteLesson = async (moduleId, lessonName) => {
    try {
      const result = await completeLesson({
        module_id: moduleId,
        lesson_name: lessonName,
        coins: 10 
      });

      if (result.coins_awarded > 0) {
        setProfile(prev => ({
          ...prev,
          coins_earned: result.new_total_coins
        }));

        setUserProgress(prev => {
          const updated = [...prev];
          const moduleProgressIndex = updated.findIndex(p => p.module_id === moduleId);
          
          if (moduleProgressIndex >= 0) {
            updated[moduleProgressIndex] = {
              ...updated[moduleProgressIndex],
              lessons_completed: [...updated[moduleProgressIndex].lessons_completed, lessonName],
              completion_percentage: result.completion_percentage
            };
          } else {
            updated.push({
              user_email: profile.email,
              module_id: moduleId,
              lessons_completed: [lessonName],
              completion_percentage: result.completion_percentage,
              last_accessed: new Date()
            });
          }
          
          return updated;
        });

        const moduleTitle = modules.find(m => m.id === moduleId)?.title || `Module ${moduleId}`;
        setRecentActivities(prev => [
          {
            module_id: moduleId,
            lesson_name: lessonName,
            coins_awarded: result.coins_awarded,
            timestamp: new Date(),
            moduleTitle: moduleTitle
          },
          ...prev.slice(0, 9) 
        ]);

        alert(`Lesson completed! You earned ${result.coins_awarded} coins!`);
      } else {
        alert('Lesson already completed!');
      }
    } catch (err) {
      console.error('Error completing lesson:', err);
      alert('Failed to complete lesson. Please try again.');
    }
  };

  const getModuleProgress = (moduleId) => {
    const progress = userProgress.find(p => p.module_id === moduleId);
    return progress ? progress.completion_percentage : 0;
  };

  const isLessonCompleted = (moduleId, lessonName) => {
    const progress = userProgress.find(p => p.module_id === moduleId);
    return progress ? progress.lessons_completed.includes(lessonName) : false;
  };

  const formatTimestamp = (timestamp) => {
    if (timestamp?.toDate) {
      return timestamp.toDate().toLocaleString();
    }
    if (timestamp instanceof Date) {
      return timestamp.toLocaleString();
    }
    return new Date(timestamp).toLocaleString();
  };

  if (!profile) return <div className="loading">Loading...</div>;

  const totalLessons = modules.reduce((sum, mod) => sum + mod.lessons.length, 0);
  const totalCompleted = userProgress.reduce((sum, progress) => sum + progress.lessons_completed.length, 0);
  const overallProgress = totalLessons ? Math.floor((totalCompleted / totalLessons) * 100) : 0;

  return (
    <div className="dashboard-container">
      <div className="left-column">
        <div className="welcome-banner">
          <h1>Hello {profile.name}!</h1>
          <div className="stats-row">
            <div className="progress-container">
              <p>Progress: {overallProgress}%</p>
              <progress className="progress-bar" value={overallProgress} max="100" />
            </div>
            <div className="coins-container">
              <p>Coins: {profile.coins_earned}</p>
            </div>
          </div>
        </div>

        <div className="recent-activity">
          <h2 >Recent Activity</h2>
          <div >
            {recentActivities.length > 0 ? (
              <div className="activities-list">
                {recentActivities.map((activity, i) => {
                  const moduleTitle = activity.moduleTitle || 
                    modules.find(m => m.id === activity.module_id)?.title || 
                    `Module ${activity.module_id}`;
                  
                  return (
                    <div key={i} className="activity-item">
                      <p><strong>{activity.lesson_name}</strong></p>
                      <p>from <em>{moduleTitle}</em></p>
                      <p className="coins-earned">+{activity.coins_awarded} coins</p>
                      <p className="activity-timestamp">
                        {formatTimestamp(activity.timestamp)}
                      </p>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div>
                No recent activity
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="right-column">
        <div className="section">
          <h2 className="section-header">Modules</h2>
          <div className="section-content">
            <div className="modules-grid">
              {modules.map((mod) => {
                const moduleProgress = getModuleProgress(mod.id);
                return (
                  <div key={mod.id} className="module-card">
                    <h3>{mod.title}</h3>
                    <p>Difficulty: {mod.difficulty}</p>
                    <p>Total Coins: {mod.total_coins}</p>
                    <p>Progress: {moduleProgress}%</p>
                    <progress className="module-progress" value={moduleProgress} max="100" />
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        <div className="section">
          <h2 className="section-header">Lessons</h2>
          <div className="section-content">
            <div className="lessons-container">
              {modules.map((mod) => (
                <div key={mod.id} className="module-lessons">
                  <div className="module-lessons-header">
                    <h4>{mod.title}</h4>
                  </div>
                  <div className="lessons-list">
                    {mod.lessons.map((lesson) => {
                      const completed = isLessonCompleted(mod.id, lesson);
                      return (
                        <div key={lesson} className={`lesson-item ${completed ? 'lesson-completed' : 'lesson-incomplete'}`}>
                          <strong>{lesson} - 10 coins</strong>
                          <div>
                            {completed ? (
                              <span className="lesson-completed-text">Done</span>
                            ) : (
                              <button 
                                className="lesson-button"
                                onClick={() => handleCompleteLesson(mod.id, lesson)}
                              >
                                Complete Lesson
                              </button>
                            )}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
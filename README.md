This is a simple navigation system code for autonomous UAV indoor flight (using computer vision technologies)      
Visual markers                                                                                                        
Image processing with OpenCV library


1.Takes off                                                                                                            
___The drone ascends.                                                                                                          
2.Follows the route                                                                                                            
___Uses Aruco markers for navigation.                                                                                          
___Sequentially visits waypoints.                                                                                              
3.Analyzes the camera image                                                                                                
___Checks if the frame contains red or green colors.                                                                                  
___If green → continues moving.                                                                                                      
___If red → performs a special action.                                                                                          
4.Completes the flight                                                                                                                    
___If the route is fully completed, the drone lands.                                                                                


Это простой код системы навигации для автономного полета БПЛА внутри помещений (с использованием технологий компьютерного зрения).      
Визуальные маркеры                                                                                                                              
Обработка изображения с библиотекой OpenCV                                                                                                      

1.Взлетает                                                                                                                                        
  Дрон поднимается.                                                                                                                                        
2.Летит по маршруту                                                                                                                                
  Использует Aruco-маркеры для навигации.                                                                                                                
  Последовательно посещает точки маршрута.                                                                                                        
3.Анализирует изображение с камеры                                                                                                                
  Проверяет, есть ли на кадре красный или зеленый цвет.                                                                                                        
  Если зеленый → продолжает движение.                                                                                                           
  Если красный → выполняет специальное действие.                                                                                                        
4.Завершает полет                                                                                                                                        
  Если маршрут пройден полностью, дрон выполняет посадку.                                                                                                

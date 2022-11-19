% Программа решающая задачу нахождения углов, необходимых для поворота
% сервоприводов двухзвенной ноги робота. 
% Также сделана визуализация процесса ходьбы
% Автор: Полторак Д.С. aka Poldi 
% Версия: 1.1.0
% Дата создания: 16.11.2022 | Дата последнего изменения: 19.11.2022

clf; % Очистка рабочей области

scale = 10;  % Масштаб изменяющий число просчитанных точек 

b     = 100; % Расстояние между ножками

% Длины звеньев ноги
l1 = 100; % Верхнее звено
l2 = 131; % Нижнее звено

% Радиус окружности траектории ходьбы
R = 0.9*l1*30/44.5;
% Смещение центра окружности 
y0 = -(R + l1*30/44.5);
x0 = 0; % x0 = -cos(pi/6) * R/2; 
% Угол, определяющий часть окружности, по которой будем ходить 
alpha = (pi/2-asin((R - l1*30/44.5)/R));

% Углы определяющие часть окружности траектории движения лапки
t = (pi/2 + alpha):-scale * pi/100:(pi/2 - alpha);

% Координаты точек окружности
xdef = (R * cos(t) + x0);
ydef = (R * sin(t) + y0);

% Дополнение для того, чтобы неточность шага не влияла
x = [xdef -xdef(1)];
y = [ydef ydef(1)];

% Горизонтальная линия
x_ = [x(length(x)):-0.9 * scale:x(1) x(1)];
y_ = [y(length(y))*ones(1, length(x_))];

scaleX1 = 0.8;  scaleX2 = 0.8;
scaleY1 = 1.4;  scaleY2 = 1.4;


%Координаты движения конца первой ножки 
X1 = [x x_ ] * scaleX1;       
Y1 = [y y_ ] * scaleY1;
Z1 = zeros(1, length(X1));

%Координаты движения конца второй ножки 
X2 = [x_ x(1) x] * scaleX2;
Y2 = [y_ y(1) y] * scaleY2;
Z2 = b*ones(1, length(X2));
maximum = length(X1);

% 1 нога %
% углы 
q2 = acos((X1.^2 + Y1.^2 - l1^2 - l2^2)/(2*l1*l2));   
q1 = atan2(Y1,X1) - atan2(l2*sin(q2),(l1+l2*cos(q2)));

% 1 звено
x1 = l1 * cos(q1);
y1 = l1 * sin(q1);

% 2 звено 
x2 = x1 + l2 * cos(q1 + q2);
y2 = y1 + l2 * sin(q1 + q2);

% 2 нога %
% углы 
q22 = acos((X2.^2 + Y2.^2 - l1^2 - l2^2)/(2*l1*l2));
q12 = atan2(Y2,X2) - atan2(l2*sin(q22),(l1+l2*cos(q22)));

% 1 звено
x12 = l1 * cos(q12);
y12 = l1 * sin(q12);

% 2 звено 
x22 = x12 + l2 * cos(q12 + q22);
y22 = y12 + l2 * sin(q12 + q22);

% Анимация ножек
for j = 1:10
      for i = 1:maximum
% %       Двухмерный случай
%         Первая ножка
%         plot(X, Y,'--k'); axis equal; grid on; hold on
%         plot(X(i), Y(i), 'o','MarkerSize',10, 'MarkerEdgeColor','red', 'MarkerFaceColor',[1 .6 .6]);
%         plot([0     x1(i)], [0     y1(i)],'-r', LineWidth=1.5); hold on
%         plot([x1(i) x2(i)], [y1(i) y2(i)],'-r', LineWidth=1.5); hold on
%         plot(X2(i), Y2(i), 'o','MarkerSize',10, 'MarkerEdgeColor','blue', 'MarkerFaceColor',[.6 .6 1]); hold on
%         plot([0      x12(i)], [0     y12(i)], '-b', LineWidth=1.5); hold on 
%         plot([x12(i) x22(i)], [y12(i) y22(i)],'-b', LineWidth=1.5); hold on

% %     Трёхмерный случай
%       Первая ножка
        plot3(X1, Z1, Y1,'--k'); axis equal; grid on; hold on 
        plot3(X1(i), Z1(i), Y1(i),'o','MarkerSize',10, 'MarkerEdgeColor','red', 'MarkerFaceColor',[1 .6 .6]); %
        plot3([0     x1(i)], [0 Z1(i)], [0     y1(i)], '-r', LineWidth=1.5); hold on
        plot3([x1(i) x2(i)], [0 Z1(i)], [y1(i) y2(i)], '-r', LineWidth=1.5); hold on
%       Вторая ножка
        plot3(X2, Z2, Y2, '--k');
        plot3(X2(i), [100 Z2], Y2(i),  'o','MarkerSize',10, 'MarkerEdgeColor','blue', 'MarkerFaceColor',[.6 .6 1]); hold on
        plot3([0      x12(i)], [100 Z2(i)], [0     y12(i)], '-b', LineWidth=1.5); hold on 
        plot3([x12(i) x22(i)], [100 Z2(i)], [y12(i) y22(i)], '-b', LineWidth=1.5); hold on

        pause(0.001)
        if i < maximum 
            clf
            i = 1;
        end
    end
end

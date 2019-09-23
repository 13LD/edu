1;
pkg load symbolic;

function xdot = f2(x, t)
  xdot=zeros(3,1);
  xdot(1) = x(2);
  xdot(2) = x(3);
  xdot(3) = 5*x(3) - 3*x(1) + sin(t);
endfunction

function return_value = Lab_2_1 (equation_number, solving_method)
  if (equation_number == 0)
    if (solving_method == "gra")
      # draw every solution simultaneously - details in each methods
      numeric_de_0 = @(t,y) [y(2); 4*y(2) + 3*y(1) - 5*cos(t)];
      [t23,y23] = ode23 (numeric_de_0, [0, 9.5], [11, 7]);
      [t45,y45] = ode45 (numeric_de_0, [0, 9.5], [11, 7]);
      syms y(x);
      symbolic_de_0 = diff(y, x, x) - 4*diff(y, x) - 3*y == -5*cos(x);
      return_cauchy = dsolve(symbolic_de_0, y(0) == 7, diff(y, 1)(0) == 11);
      ff=function_handle(rhs(return_cauchy));
      x1=0:0.45:9.5; # interval 0 to 9.5, 23 steps = 9.5/21 = 0.45
      ys=ff(x1);
      grid minor on;
      plot(t23, y23(:,1), 'rd', t45, y45(:,1), 'b*', x1, ys, 'g-');
      xlabel('x');
      legend('ode23', 'ode45', 'symbolic');
    elseif (solving_method == "rk2")
      # first we write our differential equation in numeric form and assign it
      # to a vector function; my equation is y'' - 4y' - 3y = -5cox(x)
      # y1 = y
      # y2 = y' = y1'
      # dy1/dt = y2
      # dy2/dt = 4*y2 + 3*y1 - 5*cos(t)
      numeric_de_0 = @(t,y) [y(2); 4*y(2) + 3*y(1) - 5*cos(t)];
      # next we set function to plot as it calculates itself
      opt = odeset ('RelTol', 0.01, 'AbsTol', 0.01, "InitialStep", 0.45, "MaxStep", 0.45);
      # finally, we use Runge-Kutta of order 4 and 5 to solve the equation
      # initial conditions: y'(0) = y2(0) = 11; y(0) = y1(0) = 7;
      [t,y] = ode45 (numeric_de_0, [0, 9.5], [11, 7], opt);
      return_value = [t, y];
      # semilogy(return_value);
      subplot(1,3,[1 2]);plot(t,y(:,1),'ro',t,y(:,2),'go'); xlabel('x'); legend('y',"y'");
    elseif (solving_method == "rk4")
      # first we write our differential equation in numeric form and assign it
      # to a vector function; my equation is y'' - 4y' - 3y = -5cox(x)
      # y1 = y
      # y2 = y' = y1'
      # dy1/dt = y2
      # dy2/dt = 4*y2 + 3*y1 - 5*cos(t)
      numeric_de_0 = @(t,y) [y(2); 4*y(2) + 3*y(1) - 5*cos(t)];
      # next we modify precision
      opt = odeset ('RelTol', 0.00001, 'AbsTol', 0.00001, "InitialStep", 0.45, "MaxStep", 0.45);
      # finally, we use Runge-Kutta of order 4 and 5 to solve the equation
      # initial conditions: y'(0) = y2(0) = 11; y(0) = y1(0) = 7;
      [t,y] = ode45 (numeric_de_0, [0, 9.5], [11, 7], opt);
      return_value = [t, y];
      # semilogy(return_value);
      subplot(1,3,[1 2]);plot(t,y(:,1),'ro',t,y(:,2),'go'); xlabel('x'); legend('y',"y'");
    else
      # first we declare our variables
      syms y(x);
      # then we rewrite our differential equation in symbolic form and assign it
      # to a variable; my equation is y'' - 4y' - 3y = -5cox(x)
      symbolic_de_0 = diff(y, x, x) - 4*diff(y, x) - 3*y == -5*cos(x);
      # then we attempt to solve it symbolically (analytically)
      return_value = dsolve(symbolic_de_0);
      # and its Cauchy problem (also analytically)
      return_cauchy = dsolve(symbolic_de_0, y(0) == 7, diff(y, 1)(0) == 11);
      ff=function_handle(rhs(return_cauchy));
      x1=0:0.45:9.5; # interval 0 to 9.5, 23 steps = 9.5/21 = 0.45
      y=ff(x1);
      plot(x1,y) # plot graph
      grid minor on
      # endgraph
      return_value = [return_value; return_cauchy];
    endif
  elseif (equation_number == 1)
    #y''' - 4y'' +3y = sin(x) 
    if (solving_method == "gra")
      # draw every solution simultaneously - details in each methods
      numeric_de_1 = @(t,y) [y(2); y(3); 4*y(3) - 3*y(1) + sin(t)];
      [t23,y23] = ode23 (numeric_de_1, [5, 9.5], [3, 11, 7]);
      [t45,y45] = ode45 (numeric_de_1, [5, 9.5], [3, 11, 7]);
      grid minor on;
      plot(t23, y23(:,1), 'rd', t45, y45(:,1), 'b*');
      xlabel('x');
      legend('ode23', 'ode45');
    elseif(solving_method == "rk2")
      # y1 = y
      # y2 = y' = y1'
      # y3 = y'' = y1'' = y2'
      # dy1/dt = y2
      # dy2/dt = y3
      # dy3/dt = 4*y3 - 3*y1 + sin(x)
      numeric_de_1 = @(t,y) [y(2); y(3); 4*y(3) - 3*y(1) + sin(t)];
      # next we modify precision
      opt = odeset ('RelTol', 0.00001, 'AbsTol', 0.00001, "InitialStep", 0.45, "MaxStep", 0.45);
      # finally, we use Runge-Kutta of order 2 and 3 to solve the equation
      # initial conditions: x=5; y(5)=7; y'(5)=11; y''=3 ;
      [t,y] = ode23 (numeric_de_1, [5, 9.5], [3, 11, 7], opt);
      return_value = [t, y];
      # semilogy(return_value);
      plot(t,y(:,1),'ro',t,y(:,2),'go',t,y(:,3),'bo');
      xlabel('x');
      legend('y',"y'","y''");
    elseif(solving_method == "rk2")
      # y1 = y
      # y2 = y' = y1'
      # y3 = y'' = y1'' = y2'
      # dy1/dt = y2
      # dy2/dt = y3
      # dy3/dt = 4*y3 - 3*y1 + sin(x)
      numeric_de_1 = @(t,y) [y(2); y(3); 4*y(3) - 3*y(1) + sin(t)];
      # next we modify precision
      opt = odeset ('RelTol', 0.00001, 'AbsTol', 0.00001, "InitialStep", 0.45, "MaxStep", 0.45);
      # finally, we use Runge-Kutta of order 4 and 5 to solve the equation
      # initial conditions: x=5; y(5)=7; y'(5)=11; y''=3 ;
      [t,y] = ode45 (numeric_de_1, [5, 9.5], [3, 11, 7], opt);
      return_value = [t, y];
      # semilogy(return_value);
      plot(t,y(:,1),'ro',t,y(:,2),'go',t,y(:,3),'bo');
      xlabel('x');
      legend('y',"y'","y''");
    else
      # first we declare our variables
      syms y(x);
      # then we rewrite our differential equation in symbolic form and assign it
      # to a variable; my equation is y''' - 4y'' + 3y = -5cox(x)
      symbolic_de_1 = diff(y, x, x, x) - 4*diff(y, x, x) + 3*y == sin(x);
      # then we attempt to solve it symbolically (analytically)
      return_value = dsolve(symbolic_de_1);
      # and its Cauchy task (also analytically)
      return_cauchy = dsolve(symbolic_de_1, y(5) == 7, diff(y, 1)(5) == 11, diff(y, 1, 1) == 3);
      ff=function_handle(rhs(return_cauchy));
      x1=5:0.45:9.5; # interval 0 to 9.5, 23 steps = 9.5/21 = 0.45
      y=ff(x1);
      plot(x1,y); # plot graph
      grid minor on;
      xlabel('x');
      legend('y');
      # endgraph
      return_value = [return_value; return_cauchy];
    endif
  elseif (equation_number == 2)
    #y''' - 5y'' +3y = sin(x)
    if (solving_method == "gra")
      # draw every solution simultaneously - details in each methods
      numeric_de_2 = @(t,y) [y(2); y(3); 5*y(3) - 3*y(1) + sin(t)];
      [t23,y23] = ode23 (numeric_de_2, [5, 9.5], [3, 11, 7]);
      [t45,y45] = ode45 (numeric_de_2, [5, 9.5], [3, 11, 7]);
      tls=linspace(5,9.5,21);
      x0 = [3; 11; 7];
      yls = lsode ("f2", x0, tls)
      grid minor on;
      plot(t23, y23(:,1), 'rd', t45, y45(:,1), 'b*', tls, yls(:,1), 'go');
      #plot(t, result(:,1));
      xlabel('x');
      legend('ode23', 'ode45', 'lsode');
    elseif(solving_method == "rk2")
      # y1 = y
      # y2 = y' = y1'
      # y3 = y'' = y1'' = y2'
      # dy1/dt = y2
      # dy2/dt = y3
      # dy3/dt = 5*y3 - 3*y1 + sin(x)
      numeric_de_2 = @(t,y) [y(2); y(3); 5*y(3) - 3*y(1) + sin(t)];
      # next we modify precision
      opt = odeset ('RelTol', 0.00001, 'AbsTol', 0.00001, "InitialStep", 0.45, "MaxStep", 0.45);
      # finally, we use Runge-Kutta of order 2 and 3 to solve the equation
      # initial conditions: x=5; y(5)=7; y'(5)=11; y''=3 ;
      [t,y] = ode23 (numeric_de_2, [5, 9.5], [3, 11, 7], opt);
      return_value = [t, y];
      # semilogy(return_value);
      plot(t,y(:,1),'ro',t,y(:,2),'go',t,y(:,3),'bo');
      xlabel('x');
      legend('y',"y'","y''");
    elseif(solving_method == "rk4")
      # y1 = y
      # y2 = y' = y1'
      # y3 = y'' = y1'' = y2'
      # dy1/dt = y2
      # dy2/dt = y3
      # dy3/dt = 5*y3 - 3*y1 + sin(x)
      numeric_de_2 = @(t,y) [y(2); y(3); 5*y(3) - 3*y(1) + sin(t)];
      # next we modify precision
      opt = odeset ('RelTol', 0.00001, 'AbsTol', 0.00001, "InitialStep", 0.45, "MaxStep", 0.45);
      # finally, we use Runge-Kutta of order 4 and 5 to solve the equation
      # initial conditions: x=5; y(5)=7; y'(5)=11; y''=3 ;
      [t,y] = ode23 (numeric_de_2, [5, 9.5], [3, 11, 7], opt);
      return_value = [t, y];
      # semilogy(return_value);
      plot(t,y(:,1),'ro',t,y(:,2),'go',t,y(:,3),'bo');
      xlabel('x');
      legend('y',"y'","y''");
    elseif(solving_method == "lso")
      # next we modify precision
      lsode_options ('relative tolerance', 0.000001)
      # finally, we use Runge-Kutta of order 4 and 5 to solve the equation
      # initial conditions: x=5; y(5)=7; y'(5)=11; y''=3 ;
      t=linspace(5,9.5,21);
      x0 = [3; 11; 7];
      return_value = lsode ("f2", x0, t);
      plot(return_value);
      xlabel('x');
      legend('y',"y'","y''");
    else
      # first we declare our variables
      syms y(x);
      # then we rewrite our differential equation in symbolic form and assign it
      # to a variable; my equation is y''' - 5y'' + 3y = -5cox(x)
      symbolic_de_2 = diff(y, x, x, x) - 5*diff(y, x, x) + 3*y == sin(x);
      # then we attempt to solve it symbolically (analytically)
      return_value = dsolve(symbolic_de_2);
      # and its Cauchy task (also analytically)
      return_cauchy = dsolve(symbolic_de_2, y(5) == 7, diff(y, 1)(5) == 11, diff(y, 1, 1) == 3);
      return_value = [return_value; return_cauchy];
    endif
  else
    # x'' + 9x = 10cos2t
    # mx'' + kx = Fcos(wt)
    # x_general_homogenous (t) = c1*cos(w0*t) + c2*cos(w0*t), w0 = sqrt(k/m)
    # x_partial (t) = (F0*cos(wt))/(m*(w0^2 - w^2))
    # x_general (t) = x_general_homogenous + x_partial
    # x(t) = c1*cos(w0*t) + c2*cos(w0*t) + (F0*cos(wt))/(m*(w0^2 - w^2))
    # however, if x(0) == x'(0) == 0, then
    # x(t) = F0*sin((w0-w)*t/2)*sin(w0+w)*t/2)/(m*(w0^2 - w^2))
    # k = 9, m = 1, w0 = 3
    # x(t) = F0*sin((3-w)*t/2)*sin((3+w)*t/2)/(9-w^2)
    # period is [4*pi/(3-w)]*[4*pi/(3+w)], but it seems like the product is non-preiodic
    return_value = "INPUT_ERROR";
  endif
endfunction

Lab_2_1 (0, "rk2")
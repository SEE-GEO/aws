function [f_grid,f_lims,f_chs,f0] = test_f_input(band)


switch band
  
  case '166'
    %
    f0     = 166.5e9;
    f_grid = f0 + [ -1.4 : 0.05 : 1.4 ]*1e9;
    f_lims = f0 + [ -0.8 0.8]*1e9;
    f_chs  = f0 + [ -1.4 1.4]*1e9; 
  
  case '183l'
    %
    f0     = 183.31e9;
    f_grid = f0 + [ -8 : 0.05 : -0.75 ]*1e9;
    f_lims = f0 + [ -8 -0.8]*1e9;
    f_chs  = f0 + [ -8.0 -6.0; -5.5 -3.5; -3.5 -2.5; -2.3 -1.3; -1.25 -0.75]*1e9; 

  case '229'
    %
    f0     = 229e9;
    f_grid = f0 + [ -1 : 0.05 : 1 ]*1e9;
    f_lims = f0 + [ -0.8 0.8]*1e9;
    f_chs  = f0 + [ -1 1 ]*1e9; 
  
  case '325l'
    %
    f0     = 325.15e9;
    f_grid = f0 + [ -9 : 0.05 : -0.7 ]*1e9;
    f_lims = f0 + [ -9 -0.75]*1e9;
    f_chs  = f0 + [ -9.0 -6.0; -6 -4; -4 -2; -2 -0.75]*1e9; 

  case '325u'
    %
    f0     = 325.15e9;
    f_grid = f0 + [ 0.7 : 0.05 : 9 ]*1e9;
    f_lims = f0 + [ 0.75 9]*1e9;
    f_chs  = f0 + [ 6.0 9.0; 4 6; 2 4; 0.75 2]*1e9; 
    
  otherwise
    error( 'Unknow selectio for *band*.' );
end

    


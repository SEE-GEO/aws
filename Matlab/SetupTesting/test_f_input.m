% Provides input for test_f_interp
%
% FORMAT [f_grid,f_lims,f_must,f_chs,f0] = test_f_input(band)
%
% OUT   See test_f_interp
% IN    band   Strng with band name.

% 2020-04-15 Patrick Eriksson

function [f_grid,f_lims,f_must,f_chs,f0] = test_f_input(band)

f_must = [];

switch band
  
  case '89'
    %
    f0     = 89e9;
    f_grid = f0 + [ -2 : 0.1 : 2 ]*1e9;
    f_lims = f0 + [ -1 1 ]*1e9;
    f_chs  = f0 + [ -2 2 ]*1e9; 
  
  case '166'
    %
    f0     = 165.5e9;
    f_grid = f0 + [ -1.4 : 0.05 : 1.4 ]*1e9;
    f_lims = f0 + [ -0.7 0.7 ]*1e9;
    f_chs  = f0 + [ -1.4 1.4 ]*1e9; 
  
  case '183l'
    %
    f0     = 183.311e9;
    f_grid = f0 + [ -8 : 0.05 : -0.75 ]*1e9;
    f_must = f0 + -0.75e9;
    f_lims = f0 + [ -8 -1 ]*1e9;
    f_chs  = f0 + [ -8.0 -6.0; -5.5 -3.5; -3.5 -2.5; -2.3 -1.3; -1.25 -0.75]*1e9; 

  case '229'
    %
    f0     = 229e9;
    f_grid = f0 + [ -1 : 0.05 : 1 ]*1e9;
    f_lims = f0 + [ -0.5 0.5 ]*1e9;
    f_chs  = f0 + [ -1 1 ]*1e9; 
  
  case '325l'
    %
    f0     = 325.15e9;
    f_grid = f0 + [ -9 : 0.05 : -0.75 ]*1e9;
    f_must = f0 + -0.75e9;
    f_lims = f0 + [ -9 -1]*1e9;
    f_chs  = f0 + [ -8 -5.0; -4.8 -2.3; -2.2 -1]*1e9; 
    f_chs  = f0 + [ -8 -5.2; -5.0 -3.1; -3.0 -1.7; -1.6 -0.8]*1e9; 

  case '325u'
    %
    f0     = 325.15e9;
    f_grid = f0 + [ 0.75 : 0.05 : 9 ]*1e9;
    f_must = f0 + 0.75e9;
    f_lims = f0 + [ 1 9]*1e9;
    f_chs  = f0 + [ 1 2.2; 2.3 4.8; 5 8]*1e9; 
    %f_chs  = f0 + [ 5.2 8.0; 3.1 5.0; 1.7 3.0; 0.8 1.6]*1e9; 
    
  otherwise
    error( 'Unknow selection for *band*.' );
end

    


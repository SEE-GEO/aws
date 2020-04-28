% Compiles the f_grid to apply in ARTS
%
% FORMAT f_grid = create_fgrid

% 2020-04-15 Patrick Eriksson

function f_grid = create_fgrid

r        = 0.5;
n_window = 1;
n_wing   = 7;

[f_grid,f_lims,f_must,f_chs,f0] = test_f_input( '89' );
f89 = test_f_interp(f_grid,f_lims,f_must,f_chs,r,n_window,n_window);

[f_grid,f_lims,f_must,f_chs,f0] = test_f_input( '166' );
f166 = test_f_interp(f_grid,f_lims,f_must,f_chs,r,n_window,n_window);

[f_grid,f_lims,f_must,f_chs,f0] = test_f_input( '229' );
f229 = test_f_interp(f_grid,f_lims,f_must,f_chs,r,n_window,n_window);

[f_grid,f_lims,f_must,f_chs,f0] = test_f_input( '183l' );
f183l = test_f_interp(f_grid,f_lims,f_must,f_chs,r,n_wing,n_wing);

[f_grid,f_lims,f_must,f_chs,f0] = test_f_input( '325l' );
f325l = test_f_interp(f_grid,f_lims,f_must,f_chs,r,n_wing,n_wing);

[f_grid,f_lims,f_must,f_chs,f0] = test_f_input( '325u' );
f325u = test_f_interp(f_grid,f_lims,f_must,f_chs,r,n_wing,n_wing);

f_grid = [f89,f166,f183l,f229,f325l,f325u]';
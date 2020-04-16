% Makes figures weighting functions and transmissivity to
% space for specified channels and Fascod scenario.
%
% FORMAT  mkfigs_compare_chs(atm,r_surface,chs)

% 2020-04-16 Patrick Eriksson

function mkfigs_compare_chs(atm,r_surface,chs)


%- Calculate spectra etc
%
f_fine = min(chs(:)) : 5e6 : max(chs(:))+5e6;
%
[~,J,T2S,Q] = calc_atms( atm, f_fine, r_surface );


% Channel values
%
dz = diff( p2z_simple( Q.P_GRID(4:5) ) ) / 1e3;
%
J = apply_channels( f_fine, J/(100*dz), chs );
%
T2S = apply_channels( f_fine, T2S, chs );


%- Legend texts
%
l = [];
%
for c = 1 : size(chs,1)
  l{end+1} = sprintf( '%.2f GHz', mean(chs(c,:),2)/1e9 );
end


% Plot wfuns
%
figure(1)
semilogy( J, Q.P_GRID/1e2, '-', 'LineWidth', 1 );
%
set( gca, 'YDir', 'rev' );
xlabel( 'Jacobian [K/%RH/km]' );
ylabel( 'Pressure [hPa]' );
title( upper( atm ) );
grid on;
legend( l, 'Location', 'NorthWest' );
axis([-0.025 .025 150 1000])


% Plot transmissivities
%
n = size( T2S, 2 );
%
figure(2)
semilogy( T2S, Q.P_GRID(end:-1:end-n+1)/1e2, '-', 'LineWidth', 1 );
%
set( gca, 'YDir', 'rev' );
xlabel( 'Transmissivity to space [-]' );
ylabel( 'Pressure [hPa]' );
title( upper( atm ) );
set(gca,'XTick',[0:0.1:1]);
grid on;
legend( l, 'Location', 'NorthWest' );
axis([0 1 150 1000])

return



function [Y,J,T2S,Q] = calc_atms( atm, f_grid, r_surface )
  %
  Q = q_basic( atm, f_grid, r_surface );
  %
  % Activate Jacobian for H2O
  Q.ABS_SPECIES(2).RETRIEVE = true;
  Q.ABS_SPECIES(2).GRIDS    = { Q.P_GRID, [], [] };
  Q.ABS_SPECIES(2).UNIT     = 'rel';
  % 
  Q.J_DO                    = true;
  Q.ABS_SPECIES(1).RETRIEVE = false;
  Q.ABS_SPECIES(3).RETRIEVE = false;
  %
  % Fix to get cumulative transmissivities
  workfolder    = '/home/patrick/WORKAREA';
  outfile       = fullfile( workfolder, 'ctrans.xml' );
  Q.IY_MAIN_AGENDA = { 'ppathCalc', 'iyEmissionStandard', ...
                      sprintf('WriteXML("binary",ppvar_trans_cumulat,"%s")',...
                      outfile ) };
  %
  [Y,~,J] = arts_y( Q );
  T2S     = xmlLoad( outfile )';
return

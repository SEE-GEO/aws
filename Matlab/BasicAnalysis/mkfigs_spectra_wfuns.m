% Makes figures with spectra, weighting functions and transmissivity to
% space for all bands and all five Fascod atmospheres.
%
% FORMAT  mkfigs_spectra_wfuns(r_surface,chs183,chs229,chs325)

% 2020-04-07 Patrick Eriksson

function mkfigs_spectra_wfuns(r_surface,chs183,chs229,chs325)

df = linspace( -10e9, -0.5e9, 100 );
nf = length( df );

%- 183 GHz
%
c183 = 183.31e9;
f183 = c183 + df;
%
[Y183,J183,T183,atms,Q] = calc_atms( f183, r_surface );

%- 325 GHz
%
c325 = 325.15e9;
f325 = c325 + df;
ftmp = c325 + [df sort(-df) ];
%
[Y325,J325,T325] = calc_atms( ftmp, r_surface );
%
Y325 = ( Y325(1:nf,:) + Y325(nf*2:-1:nf+1,:) ) / 2;
T325 = ( T325(1:nf,:,:) + T325(nf*2:-1:nf+1,:,:) ) / 2;
J325 = ( J325(1:nf,:,:) + J325(nf*2:-1:nf+1,:,:) ) / 2;

%- 229 GHz
%
df   = linspace( -1e9, -0.1, 10 );
nf   = length( df );
c229 = 229e9;
f229 = c229 + df;
ftmp = c229 + [df sort(-df) ];
%
[Y229,J229,T229] = calc_atms( ftmp, r_surface );
%
Y229 = ( Y229(1:nf,:) + Y229(nf*2:-1:nf+1,:) ) / 2;
T229 = ( T229(1:nf,:,:) + T229(nf*2:-1:nf+1,:,:) ) / 2;
J229 = ( J229(1:nf,:,:) + J229(nf*2:-1:nf+1,:,:) ) / 2;


%- Spectrum plot
%
figure(1)
clf
h1 = plot( (f183-c183)/1e9, Y183, '-', 'LineWidth', 1 );
hold on
set( gca, 'ColorOrderIndex', 1 );
h2 =plot( (f229-c229)/1e9, Y229, '-.', 'LineWidth', 1 );
set( gca, 'ColorOrderIndex', 1 );
h3 = plot( (f325-c325)/1e9, Y325, '--', 'LineWidth', 1 );
xlabel( 'Distance from reference frequency [GHz]' );
ylabel( 'Tb [K]' );
grid on
%
l        = upper( atms );
l{1}     = [ l{1}, ', 183 GHz'];
l{end+1} = '229 GHz';
l{end+1} = '325 GHz';
%
legend( [h1;h2(1);h3(1)], l, 'Location', 'South' );
hold off
%
axis([ -10 0 230 286 ])


% Wfuns plots
%
dz = diff( p2z_simple( Q.P_GRID(4:5) ) ) / 1e3;
%
for i = 1 : length(atms)
  figure( get(gcf,'Number') + 1 );
  clf;
  n = size( T183, 2 );
  l = {};
  %
  D = apply_channels( f183, J183(:,:,i)/(100*dz), chs183 );
  semilogy( D, Q.P_GRID/1e2, '-', 'LineWidth', 1 );
  hold on
  for c = 1 : size(chs183,1)
    l{end+1} = sprintf( 'AWS-3%d', c+1 );
  end
  set( gca, 'ColorOrderIndex', 1 );
  %
  D = apply_channels( f229, J229(:,:,i)/(100*dz), chs229 );
  semilogy( D, Q.P_GRID/1e2, '-.', 'LineWidth', 1 );
  l{end+1} = 'AWS-41';
  %
  D = apply_channels( f325, J325(:,:,i)/(100*dz), chs325 );
  semilogy( D, Q.P_GRID/1e2, '--', 'LineWidth', 1 );
  for c = 1 : size(chs325,1)
    l{end+1} = sprintf( 'ICI-%d', c+4 );
  end
  set( gca, 'ColorOrderIndex', 1 );
  %
  set( gca, 'YDir', 'rev' );
  xlabel( 'Jacobian [K/%RH/km]' );
  ylabel( 'Pressure [hPa]' );
  title( upper( atms{i} ) );
  grid on;
  legend( l, 'Location', 'NorthEast' );
  axis([-0.025 .025 150 1000])
end


% Transmission to space plots
%
for i = 1 : length(atms)
  figure( get(gcf,'Number') + 1 );
  clf;
  n = size( T183, 2 );
  l = {};
  %
  D = apply_channels( f183, T183(:,:,i), chs183 );
  semilogy( D, Q.P_GRID(end:-1:end-n+1)/1e2, '-', 'LineWidth', 1 );
  hold on
  for c = 1 : size(chs183,1)
    l{end+1} = sprintf( 'AWS-3%d', c+1 );
  end
  set( gca, 'ColorOrderIndex', 1 );
  %
  D = apply_channels( f229, T229(:,:,i), chs229 );
  semilogy( D, Q.P_GRID(end:-1:end-n+1)/1e2, '-.', 'LineWidth', 1 );
  l{end+1} = 'AWS-41';
  %
  D = apply_channels( f325, T325(:,:,i), chs325 );
  semilogy( D, Q.P_GRID(end:-1:end-n+1)/1e2, '--', 'LineWidth', 1 );
  for c = 1 : size(chs325,1)
    l{end+1} = sprintf( 'ICI-%d', c+4 );
  end
  set( gca, 'ColorOrderIndex', 1 );
  %
  set( gca, 'YDir', 'rev' );
  xlabel( 'Transmissivity to space [-]' );
  ylabel( 'Pressure [hPa]' );
  title( upper( atms{i} ) );
  set(gca,'XTick',[0:0.1:1]);
  grid on;
  legend( l, 'Location', 'NorthWest' );
  axis([0 1 150 1000])
end

return


function [Y,J,T2S,atms,Q] = calc_atms( f_grid, r_surface )
  %
  atms = { 'tro', 'mls', 'mlw', 'sas', 'saw' };
  %
  Y = zeros( length(f_grid), length(atms) );
  %
  for i = 1 : length(atms)
    %
    Q             = q_basic( atms{i}, f_grid, r_surface );
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
    [Y(:,i),~,J(:,:,i)] = arts_y( Q );
    T2S(:,:,i)          = xmlLoad( outfile )';
  end
return

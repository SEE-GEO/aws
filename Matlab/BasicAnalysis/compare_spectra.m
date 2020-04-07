function compare_spectra(r_surface,chs183,chs229,chs325)

df = linspace( -10e9, -0.5e9, 50 );
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
T325 = ( T325(:,1:nf,:) + T325(:,nf*2:-1:nf+1,:) ) / 2;

%- 229 GHz
%
df   = linspace( -1e9, -0.1, 5 );
nf   = length( df );
c229 = 229e9;
f229 = c229 + df;
ftmp = c229 + [df sort(-df) ];
%
[Y229,J229,T229] = calc_atms( ftmp, r_surface );
%
Y229 = ( Y229(1:nf,:) + Y229(nf*2:-1:nf+1,:) ) / 2;


%- Spectrum plot
%
figure(1)
clf
h1 = plot( (f183-c183)/1e9, Y183, '-', 'LineWidth', 1 );
hold on
set( gca, 'ColorOrderIndex', 1 );
h2 = plot( (f325-c325)/1e9, Y325, '--', 'LineWidth', 1 );
set( gca, 'ColorOrderIndex', 1 );
h3 =plot( (f229-c229)/1e9, Y229, '-.', 'LineWidth', 1 );
xlabel( 'Distance from centre/LO frequency [GHz]' );
ylabel( 'Tb [K]' )
%
l        = upper( atms );
l{1}     = [ l{1}, ', 183 GHz'];
l{end+1} = '325 GHz';
l{end+1} = '229 GHz';
%
legend( [h1;h2(1);h3(1)], l, 'Location', 'SouthWest' );
hold off
%
axis([ -10 0 230 286 ])


% Transmission to space plots
%
for i = 1 : length(atms)
  figure(1+i);
  clf;
  n = size( T183, 1 );
  l = {};
  %
  D = apply_channels( f183, T183(:,:,i), chs183 );
  semilogy( D, Q.P_GRID(end:-1:end-n+1)/1e2, '-', 'LineWidth', 1 );
  hold on
  for c = 1 : size(chs183,1)
    l{end+1} = sprintf( '183 / %d', c );
  end
  set( gca, 'ColorOrderIndex', 1 );
  %
  D = apply_channels( f325, T325(:,:,i), chs325 );
  semilogy( D, Q.P_GRID(end:-1:end-n+1)/1e2, '--', 'LineWidth', 1 );
  for c = 1 : size(chs325,1)
    l{end+1} = sprintf( '325 / %d', c );
  end
  set( gca, 'ColorOrderIndex', 1 );
  %
  D = apply_channels( f229, T229(:,:,i), chs229 );
  semilogy( D, Q.P_GRID(end:-1:end-n+1)/1e2, '-.', 'LineWidth', 1 );
  l{end+1} = '229';
  %
  set( gca, 'YDir', 'rev' );
  xlabel( 'Transmissivity to space [-]' );
  ylabel( 'Pressure [hPa]' );
  title( upper( atms{i} ) );
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
    % Fix to get cumulative transmissivities
    workfolder    = '/home/patrick/WORKAREA';
    outfile       = fullfile( workfolder, 'ctrans.xml' );
    Q.IY_MAIN_AGENDA = { 'ppathCalc', 'iyEmissionStandard', ...
                 sprintf('WriteXML("binary",ppvar_trans_cumulat,"%s")',...
                         outfile ) };
    %
    [Y(:,i),~,J]  = arts_y( Q );
    T2S(:,:,i)    = xmlLoad( outfile );
  end
return

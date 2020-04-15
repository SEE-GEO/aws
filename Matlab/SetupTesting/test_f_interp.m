% Testing of frequencies to apply
%
% FORMAT f_n = test_f_interp(f_grid,f_lims,f_chs,r_surface,nmax,nout)
%
% OUT   f_n      Frequency grid applied for nout
% IN    f_grid   Fine grid. Data on this grid represents the truth. Should
%                cover all other frequencies.
%       f_lims   Frequency limits for equidistant sparse grid.
%       f_chs    Edge frequencies for each channel to evaluate. One row per channel.
%       r_surface  Surface reflectivity.
%       nmax     Max points in sparse grid to consider
%       nout     Return f_n and make plot for this n.

% 2020-04-15 Patrick Eriksson

function f_n = test_f_interp(f_grid,f_lims,f_chs,r_surface,nmax,nout)

%- Get reference spectrum
%
Y0 = calc_atms( f_grid, r_surface );


%- Special case of empty f_lims
%
if isempty(f_lims)
  [nstart,nmax,nout] = deal( size(f_chs,1) );
else
  nstart = 1;
end
    

%- Test with different n
%
fprintf('\n             Full band                   Channel\n')
fprintf(' n    mean      std      max     mean      std      max\n')
fprintf('-------------------------------------------------------\n')
%
for n = nstart : nmax
  if isempty(f_lims)
    f_test    = mean( f_chs, 2 )';
  elseif n == 1
    f_test   = (f_lims(1) + f_lims(end)) / 2;
  else
    f_test   = linspace( f_lims(1), f_lims(end), n );
  end
  [Y,atms] = calc_atms( f_test, r_surface );
  if 0
    imethod = 'spline';
    if n == 1
      dY      = repmat( Y, length(f_grid), 1 );
    else
      dY      = interp1( f_test, Y, f_grid, imethod, 'extrap' ) ;
    end
    stitle  = sprintf( '%s-interpolation', imethod );
  else
    dY = zeros(size(Y0));
    for j = 1 : length(atms)
      [p,~,mu] = polyfit( vec2col(f_test), Y(:,j), n-1 );
      dY(:,j)  = polyval( p, (f_grid-mu(1))/mu(2) )'; 
    end
    stitle = 'polyfit';
  end
  %
  Ce = zeros( size(f_chs,1), length(atms) );
  for j = 1 : size(f_chs,1)
    ind     = find( f_grid >= f_chs(j,1) & f_grid <= f_chs(j,2) );
    Ce(j,:) = mean( dY(ind,:)-Y0(ind,:), 1 );
  end
  %
  dY     = dY - Y0;
  %
  if n == nout
    f_n = f_test;
    if ~nargout
      plot( f_grid/1e9, dY );
      grid on;
      xlabel( 'Frequency [GHz]' );
      ylabel( 'Interpolatio error [K]' ); 
      title( sprintf('%s with %d points',stitle,n) );
      legend( upper(atms), 'Location', 'South' );
      drawnow;
    end
  end
  %
  dY = dY(:);
  %
  fprintf( '%02d: %+4.2fK / %5.2fK / %5.2fK / %5.2fK / %5.2fK / %5.2fK\n', ...
           n, mean(dY), std(dY), max(abs(dY)), ...
           mean(Ce(:)), std(Ce(:)), max(abs(Ce(:))) );

end

fprintf('-------------------------------------------------------\n')


return


function [Y,atms] = calc_atms( f_grid, r_surface )
  %
  atms = { 'tro', 'mls', 'mlw', 'sas', 'saw' };
  %
  Y = zeros( length(f_grid), length(atms) );
  %
  for i = 1 : length(atms)
    Q      = q_basic( atms{i}, f_grid, r_surface );
    Y(:,i) = arts_y( Q );
  end
return

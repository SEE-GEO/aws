% FORMAT C = extract_cases(S,ATM)
%
% OUT   C     Structure array of case data
% IN    S     Project settings structure
%       ATM   Structure with atmospheric data.

% 2020-03-25 Patrick Eriksson

function C = extract_cases(S,ATM)

% Start index of each case 
%
ic1 = 1 : S.cases.nalong : (length(ATM.lat_grid)-S.cases.nalong+1);

% Some variables to handle that longitudes can be both [-180,180] and [0,360]
%
[~,lonlow1,lonhigh1] = set_lon_limits( ATM.t_skin.grids{2} );
[~,lonlow2,lonhigh2] = set_lon_limits( ATM.surftype.grids{2} );
[~,lonlow3,lonhigh3] = set_lon_limits( ATM.wind_speed.grids{2} );
[~,lonlow4,lonhigh4] = set_lon_limits( ATM.wind_direction.grids{2} );

% Convert to linear reflectivites and with non-significant returns set to zero
%
R = 10.^(ATM.Radar_Reflectivity/10);
R(R==min(R)) = 0;



C = [];

for i = 1 : length(ic1)
  %
  ind = ic1(i) + (0:S.cases.nalong-1);
  im = ic1(i) + floor(S.cases.nalong/2);
  %
  if all( ATM.DEM_elevation(ind) < S.cases.zsurf_max )

    iout = length(C) + 1;

    % Position 
    C(iout).lat        = ATM.lat_grid(im);
    C(iout).lon        = ATM.lon_grid(im);
    
    % Surface variables
    C(iout).z_surface  = ATM.DEM_elevation(im);    
    %
    lonp               = shift_longitudes( C(iout).lon, lonlow2, lonhigh2 );
    C(iout).i_surface  = round( pointinterp( ATM.surftype.grids, ...
                                             ATM.surftype.data, ...
                                             [C(iout).lat,lonp] ) );
    %
    lonp               = shift_longitudes( C(iout).lon, lonlow1, lonhigh1 );
    C(iout).t_surface  = pointinterp( ATM.t_skin.grids, ...
                                      ATM.t_skin.data, ...
                                      [C(iout).lat,lonp] );
    %
    lonp               = shift_longitudes( C(iout).lon, lonlow3, lonhigh3 );
    C(iout).wind_speed = pointinterp( ATM.wind_speed.grids, ...
                                      ATM.wind_speed.data, ...
                                      [C(iout).lat,lonp] );
    %
    lonp               = shift_longitudes( C(iout).lon, lonlow4, lonhigh4 );
    C(iout).wind_dir   = pointinterp( ATM.wind_direction.grids, ...
                                      ATM.wind_direction.data, ...
                                      [C(iout).lat,lonp] );

    % "Clear-sky" variables
    %
    iz                 = find( ATM.z_field(:,im) > C(iout).z_surface );
    C(iout).z_field    = [ C(iout).z_surface; ATM.z_field(iz,im) ];
    %
    C(iout).p_grid     = exp( interp1( ATM.z_field(:,im), log(ATM.p_grid), ...
                                       C(iout).z_field ) );    
    C(iout).t_field    = interp1( ATM.z_field(:,im), ATM.t_field(:,im), ...
                                  C(iout).z_field );
    C(iout).h2o        = interp1( ATM.z_field(:,im), ATM.h2o_field(:,im), ...
                                  C(iout).z_field );
    C(iout).lwc        = interp1( ATM.z_field(:,im), ATM.lwc_field(:,im), ...
                                  C(iout).z_field );
    
    % Reflectivites
    C(iout).dBZ        = 10 * log10( [ 1e-10; max( mean( R(iz,ind), 2 ), 1e-10) ] );

    % IWC and RWC
    if isfield( ATM, 'IWC' )
      C(iout).rwc_psd   = ATM.particle_model(1).psd.name;
      C(iout).rwc_habit = ATM.particle_model(1).habit.name;
      C(iout).rwc       = interp1( ATM.z_field(:,im), ATM.RWC(:,im), ...
                                   C(iout).z_field );
      C(iout).iwc_psd   = ATM.particle_model(2).psd.name;
      C(iout).iwc_habit = ATM.particle_model(2).habit.name;
      C(iout).iwc       = interp1( ATM.z_field(:,im), ATM.IWC(:,im), ...
                                   C(iout).z_field );
    end
  end
end
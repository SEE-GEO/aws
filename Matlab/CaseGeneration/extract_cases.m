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
    C(iout).i_surface  = pointinterp( ATM.surftype.grids, ...
                                      ATM.surftype.data, ...
                                      [C(iout).lat,lonp] );
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
    C(iout).p_grid     = ATM.p_grid;
    C(iout).z_field    = ATM.z_field(:,im);
    C(iout).t_field    = ATM.t_field(:,im);
    C(iout).h2o        = ATM.h2o_field(:,im);
    C(iout).lwc        = ATM.lwc_field(:,im);
    
    % Reflectivites
    C(iout).dBZ        = 10 * log10( max( mean( R(:,ind), 2 ), 1e-10) );
    
  end
end
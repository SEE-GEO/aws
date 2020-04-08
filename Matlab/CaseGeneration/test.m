%- Set work folder to use
%
switch whoami
  case 'patrick'
    workfolder  = '/home/patrick/WORKAREA';
    do_radarinv = false;
  case 'inderpreet'
    workfolder  = 'home/inderpreet/Projects/AWS'
    do_radarinv = false;
  otherwise
    error( 'Unknown user' );
end  


%- General settings
%
S = s_default;

%- Define orbit part to process
%
year  = 2015;
doy   = 204;
ifile = 12;
S.csat.filename = find_csat_files( S, year, doy, ifile );
%
S.csat.lat_lims    = [ 5 11 ];
S.csat.orbitleg    = 2;

%- Get 2D atmospheric view
%
ATM = extract_atm2d( S, workfolder, do_radarinv );

%- Extract individual cases
%
C = extract_cases( S, ATM );

%- Save to file
%
filename = sprintf('c_of_%04d_%03d_%02d', year, doy, ifile );
%
save( filename, '-v7.3', 'C' );
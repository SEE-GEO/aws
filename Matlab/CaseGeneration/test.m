%- Set work folder to use
%
switch whoami
  case 'patrick'
    workfolder = '/home/patrick/WORKAREA';
  otherwise
    error( 'Unknown user' );
end  


%- General settings
%
S = settings;

%- Define orbit part to process
%
S.csat.filename = find_csat_files( S, 2015, 204, 12 );
%
S.csat.lat_lims    = [ 5 11 ];
S.csat.orbitleg    = 2;

%- Get 2D atmospheric view
%
ATM = extract_atm2d( S, workfolder );

%- Extract individual cases
%
C = extract_cases( S, ATM );
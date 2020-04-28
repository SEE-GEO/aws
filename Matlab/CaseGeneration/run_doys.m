% FORMAT run_doys(year,doys[,lat_lims])
%
%    Creates cases for a set of DOYS (inside a single year).
%
%    Some stuff is hard-coded.
%
% IN   year      Year
%      doys      A vector with day-of-years
% OPT  lat_lims  Latitude limites. Default is [-60,60].

function run_doys(year,doys,lat_lims)
%
if nargin < 3, lat_lims = [-60 60]; end  


%- Set work folder to use
%
switch whoami
  case 'patrick'
    workfolder  = '/home/patrick/WORKAREA';
    dendrite    = '/home/patrick/Dendrite';
  case 'inderpreet'
    workfolder  = 'home/inderpreet/Projects/AWS'
    dendrite    = '~/Dendrite';  % Correct ???
  otherwise
    error( 'Unknown user' );
end  


%- General settings
%
S = s_default;
%
S.csat.lat_lims    = lat_lims;
S.csat.orbitleg    = 2;
%
do_radarinv        = false;


%- Loop doys and files of the day
%
for doy = vec2row(doys)

  for ifile = 1 : 16

    %- Get full file name
    %
    S.csat.filename = find_csat_files( S, year, doy, ifile );

    
    if ~isempty(S.csat.filename)

      try

        fprintf( 'Doing %04d/%03d/%02d\n', year, doy, ifile );

        %- Get 2D atmospheric view
        %
        ATM = extract_atm2d( S, workfolder, do_radarinv );

        %- Extract individual cases
        %
        C = extract_cases( S, ATM );

        %- Save to file
        %
        filename = fullfile( dendrite, 'Projects/AWS-325GHz/Cases_m60_p60', ...
                             sprintf('c_of_%04d_%03d_%02d', year, doy, ifile  ) );
        %
        save( filename, '-v7.3', 'C' );
      
      catch
        fprintf( '!!! Failure the file above !!!\n', year, doy, ifile );
      end
      
    end
  end
end

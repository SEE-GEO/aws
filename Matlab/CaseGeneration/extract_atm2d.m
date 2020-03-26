% EXTRACT_ATM2D   Reads and merges CloudSat and ERA-Interim
%
%   Most data come out on a common grid. The vertical grid is determined by
%   S.p_grid while the along-track one follows the CloudSat data. Some
%   surface variables are included as gridded data (on seperate grids).
%  
%   The ATM structure has these fields (with example sizes):
%               p_grid: [75x1 double]
%              lat_grid: [620x1 double]
%              lon_grid: [620x1 double]
%               z_field: [75x620 double]
%               t_field: [75x620 double]
%             h2o_field: [75x620 double]
%             lwc_field: [75x620 double]
%                   dim: 2
%                   mjd: 5.7227e+04
%         DEM_elevation: [620x1 double]
%        CPR_Cloud_mask: [75x620 double]
%    Radar_Reflectivity: [75x620 double]
%                t_skin: [1x1 struct]
%            wind_speed: [1x1 struct]
%        wind_direction: [1x1 struct]
%              surftype: [1x1 struct]
%
% FORMAT ATM = extract_atm2d(S,workfolder)
%
% OUT  ATM   Structure with CloudSat, surface and atmospheric data
%      S     Setting structure
%      workfolder   The function will unpack CloudSat zipped files here
%                   Avoid running several processing on same CloudSat orbit, 
%                   using the same workfolder.

% 2020-03-25 Patrick Eriksson

function ATM = extract_atm2d(S,workfolder)

%- Import specified CloudSat data
%
CSAT = import_csat( S, workfolder );

%- Filter reflectivities
%
CSAT = filter_dbz( CSAT, S.csat.dbz_limit, S.csat.cmask_limit );

%- Extract matching atmospheric data from ERA
%
ERA = csat2era( CSAT, S );

%- Merge CloudSat with ERA. This includes
%  interpolation to the pressure grid selected
%
ATM = csat2atmdata( CSAT, ERA );

%- Add needed surface variables:
%
ATM = atm_add_erasurf( ATM, 1 );
ATM = atm_add_surftype( ATM, [], 0.1 );




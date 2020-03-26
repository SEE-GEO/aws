% SETTINGS   Project settings
%
%   General and hard-coded setings of the project
%
% FORMAT  S = settings

function  S = settings


% 2D part
% -------
%
% Vertical grid of data
S.p_grid           = z2p_simple( -500 : 250 : 18e3 )';
%
% Settings around CloudSat
S.csat.folder      = '~/Dendrite/SatData/CloudSat';
S.csat.product     = '2B-GEOPROF';
S.csat.cmask_limit = 20;             % Cloud mask threshold value.
S.csat.dbz_limit   = -27;            % Minimum dBZ to allow.


% Case creation
% -------------
%
% Number of CloudSat profiles to average (approax 1km/profile)
S.cases.nalong     = 10; 
%
% Highest allowed surface altitude
S.cases.zsurf_max  = 500;;       
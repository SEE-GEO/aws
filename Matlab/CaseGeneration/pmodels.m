% PMODELS  Particle model settings
%
%   With output argument, the function returns the particle model settings
%   used in the project.
%
%   Without output argumens, radar inversion tables are produced.
%
% FORMAT [FPI,PMS] = pmodels

% 2020-03-31 Patrick Eriksson

function [FPI,PMS] = pmodels

% Default settings (for CloudArts)
%
FPI = fpi_settings;

% Select other folder for radar tables
%
FPI.table_folder  = '/home/patrick/Outdata2/AWS/RadarTables';



% Read pre-defined particle models
%
Pl  = liq_pmodels;
Pi  = ice_pmodels( 'strdhab_mat', '~/Outdata2/ScatData/StandardHabits' );

% Check and extract 
%
il = 3;
ii = 3*length(Pi)/4 + 1;
%
if ~strcmp( Pl(il).psd.name, 'wang16' )
  error( 'WangEtAl16 not found among liquid pmodels.' );
end
%
if ~strcmp( Pi(ii).psd.name, 'dardar-apriori' )
  error( 'F07t not found among ice pmodels.' );
end
%
Pl = Pl(il);
Pi = Pi(ii);

% Set particle models
%
Pi.habit.name = 'Perpendicular3BulletRosette';
PMS{1} = [ Pl, Pi ];
%
Pi.habit.name = 'LargePlateAggregate';
PMS{2} = [ Pl, Pi ];
%
Pi.habit.name = 'LargeColumnAggregate';
PMS{3} = [ Pl, Pi ];

if nargout, return, end


% Create radar inversion tables
%
% Liquid pmodels
create_and_store_fpi_table( FPI, PMS{1}(1) );
% 
% Ice pmodels
for i = 1 : length(PMS)
  create_and_store_fpi_table( FPI, PMS{i}(2) );
end
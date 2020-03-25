% INIT_PROJECT   Needed initialisations
%
%    Run this function at start of each session.
%
% FORMAT init_aws325ghz

% 2020-03-25 Patrick Eriksson

function init_aws325ghz

% Include CloudArts in search path
%
switch whoami
  case 'patrick'
    run( '~/SVN/opengem/patrick/Projects/CloudArts/addpath_cloudarts' );
  otherwise
    error( 'Unknown user' );
end


% Required atmlab settings
%
atmlab( 'SITE', 'chalmers-gem' );
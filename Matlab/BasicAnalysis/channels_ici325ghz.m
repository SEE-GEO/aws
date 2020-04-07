% Returns limits for ICI 325 GHz channels
%
%    Limits for lower sideband returned
%
% FORMAT chs325 = channels_ici325ghz
%
% OUT   chs325  Limits for lower sideband of ICI 325 GHz channels

% 2020-04-07 Patrick Eriksson

function chs325 = channels_ici325ghz

chs325 = 325.15e9 + [-11.0 -8.00;
                     -4.70 -2.30;
                     -2.30 -0.70 ] * 1e9;

% Returns limits for fixed chanels
%
% FORMAT [chs183,ch229] = channels_fixed
%
% OUT   chs183  Limits for lower sideband of MWS 183 GHz channels
%       chs229  Limits  of MWS 229 GHz channel

% 2020-04-07 Patrick Eriksson

function [chs183,ch229] = channels_fixed

chs183 = 183.31e9 + [-8.00 -6.00;
                     -5.50 -3.50;
                     -3.50 -2.50;
                     -2.30 -1.30;
                     -1.25 -0.75 ] * 1e9;

ch229 = [228e9 230e9];

% Set channels
%
[chs183,ch229] = channels_fixed;
chs325         = channels_ici325ghz;

% Results for r = 0
%
mkfigs_spectra_wfuns( 0, chs183, ch229, chs325 );
%
print -f1 fascod_tb_r000.pdf -dpdf


% Results for r = 0.5
%
mkfigs_spectra_wfuns( 0.5, chs183, ch229, chs325 );
%
print -f1 fascod_tb_r050.pdf -dpdf



!pdfcropbatch *.pdf
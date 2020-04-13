
% Set channels
%
[chs183,ch229] = channels_fixed;
chs325         = channels_ici325ghz;

if 0
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
end

% Results for r = 0.25
%
mkfigs_spectra_wfuns( 0.25, chs183, ch229, chs325 );
%
print -f3 fascod_wf_mls_025.pdf -dpdf
print -f8 fascod_tr_mls.pdf -dpdf



!pdfcropbatch *.pdf
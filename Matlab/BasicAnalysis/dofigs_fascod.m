%----------------------------------------------
%--- Compare bands
%----------------------------------------------

if 0

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

% Results for r = 0.25
%
mkfigs_spectra_wfuns( 0.25, chs183, ch229, chs325 );
%
print -f3 fascod_wf_mls_025.pdf -dpdf
print -f8 fascod_tr_mls.pdf -dpdf

end


%----------------------------------------------
%--- Wfuns in wingds of 183 and 325 GHz
%----------------------------------------------

chs=325.15e9+[-12 -10;-10 -8;-8 -6;-6 -4;-4 -2;-2 -1]*1e9;
%
mkfigs_compare_chs( 'tro', 0.1, chs );
%
figure(1)
axis([-0.025 0 150 1000])
%
print -f1 fascod_wf_325l_tro.pdf -dpdf

chs=325.15e9+[10 12;8 10;6 8;4 6; 2 4;1 2]*1e9;
%
mkfigs_compare_chs( 'tro', 0.1, chs );
%
figure(1)
axis([-0.025 0 150 1000])
%
print -f1 fascod_wf_325u_tro.pdf -dpdf


!pdfcropbatch *.pdf
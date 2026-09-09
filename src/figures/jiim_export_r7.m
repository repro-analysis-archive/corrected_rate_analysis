function jiim_export_r7(fig, name, outdir)
% Same .fig -> vector PDF + 600 dpi TIFF. Export gcf so annotation panel labels survive.
assert(any(strcmpi(listfonts,'Arial')), 'Arial is not available; stop before rendering.');
set(findall(fig,'-property','FontName'),'FontName','Arial');
set(fig,'Color',[1 1 1],'InvertHardcopy','off','PaperPositionMode','auto');
if ~exist(outdir,'dir'), mkdir(outdir); end
savefig(fig, fullfile(outdir, [name '.fig']));
% 'Padding','figure' keeps the FULL declared canvas; the default tight crop
% shrinks the exported width below the 174 mm design width (measured 158.5-167.3 mm).
exportgraphics(fig, fullfile(outdir, [name '.pdf']), 'ContentType','vector', ...
               'Resolution',600, 'Padding','figure');
exportgraphics(fig, fullfile(outdir, [name '.tif']), 'Resolution',600, 'Padding','figure');
fprintf('exported %s (.fig/.pdf/.tif)\n', name);
end

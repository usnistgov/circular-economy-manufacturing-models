
document.addEventListener('DOMContentLoaded', function (){
	const img = document.querySelector('img[usemap]');
	if (!img) return;

	const imgmap = document.querySelector("map[name='sitemap']");
	if (!imgmap) return;

	const areas = imgmap.querySelectorAll('area');
	
	const origWidth = img.naturalWidth;
	const origHeight = img.naturalHeight;
	
	function scaleMap(){
		const curWidth = img.clientWidth;
		const curHeight = img.clientHeight;
		const widthratio = curWidth/origWidth;
		const heightratio = curHeight/origHeight;
		
		areas.forEach(area => {
			const origCoords = area.dataset.origCoords || area.getAttribute('coords');
			area.dataset.origCoords = origCoords;
			
			const scaledCoords = origCoords.split(',').map((coord, index) => {
				return index % 2 === 0
					? Math.round(coord * widthratio)
					: Math.round(coord * heightratio);
			
			});
			area.setAttribute('coords', scaledCoords.join(','));
		});

	}
	
	scaleMap();
	window.addEventListener('resize', scaleMap);
});

document.onreadystatechange = function(){
	if (document.readyState === 'complete'){
		const img = document.querySelector('img[usemap]');
		if (!img) return;

		const imgmap = document.querySelector("map[name='sitemap']");
		if (!imgmap) return;

		const areas = imgmap.querySelectorAll('area');
			
		const origWidth = img.naturalWidth;
		const origHeight = img.naturalHeight;
			
		function scaleMap(){
			const curWidth = img.clientWidth;
			const curHeight = img.clientHeight;
			const widthratio = curWidth/origWidth;
			const heightratio = curHeight/origHeight;
				
			areas.forEach(area => {
				const origCoords = area.dataset.origCoords || area.getAttribute('coords');
				area.dataset.origCoords = origCoords;
					
				const scaledCoords = origCoords.split(',').map((coord, index) => {
					return index % 2 === 0
						? Math.round(coord * widthratio)
						: Math.round(coord * heightratio);
					
				});
				area.setAttribute('coords', scaledCoords.join(','));
			});
		}
			
		scaleMap();
		window.addEventListener('resize', scaleMap);
	}
}
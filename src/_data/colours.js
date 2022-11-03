import { ColourScale } from 'local/oi/colours.js';

export const colours = {
	"Gold": "#F7AB3D","Gold-1": "#f9bc64","Gold-2": "#facd8b","Gold-3": "#fcddb1","Gold-4": "#fdeed8",
	"Orange": "#E55912","Orange-1": "#eb7a41","Orange-2": "#f09c71","Orange-3": "#f5bda0","Orange-4": "#faded0",
	"Turquoise": "#69C2C9","Turquoise-1": "#87ced4","Turquoise-2": "#a5dadf","Turquoise-3": "#c3e7ea","Turquoise-4": "#e1f3f4",
	"Cherry": "#E52E36","Cherry-1": "#eb585e","Cherry-2": "#f08286","Cherry-3": "#f5abae","Cherry-4": "#fad5d7",
	"Chartreuse": "#C7B200","Chartreuse-1": "#d2c233","Chartreuse-2": "#ddd166","Chartreuse-3": "#e9e099","Chartreuse-4": "#f4f0cc",
	"Plum": "#7D2248","Plum-1": "#974e6d","Plum-2": "#b17a91","Plum-3": "#cba7b6","Plum-4": "#e5d3da",
	"Grey": "#B2B2B2","Grey-1": "#c1c1c1","Grey-2": "#d1d1d1","Grey-3": "#e0e0e0","Grey-4": "#f0f0f0",
	"Blue": "#005776","Blue-1": "#337991","Blue-2": "#669aad","Blue-3": "#99bcc8","Blue-4": "#ccdde4",
	"Raisin": "#874245","Raisin-1": "#9f686a","Raisin-2": "#b78e8f","Raisin-3": "#cfb4b5","Raisin-4": "#e7d9da",
	"Rose": "#FF808B","Rose-1": "#ff9aa2","Rose-2": "#ffb3b9","Rose-3": "#ffccd1","Rose-4": "#ffe6e8",
	"Forest": "#4A783C","Forest-1": "#6e9363","Forest-2": "#92ae8a","Forest-3": "#b7c9b1","Forest-4": "#dbe4d8",
	"Black": "#000000","Black-1": "#595b61","Black-2": "#85878b","Black-3": "#b0b1b3","Black-4": "#d8d9da",
	// Genders
	"Female":"#ee7e3b",
	"Male":"#264c59",
	// Ethnicities
	"Bangladeshi":"#7D2248","Black/African/Caribbean/Black British":"#75b8d3","Chinese":"#fe9400", "Indian":"#274b57","Mixed/Multiple":"#E55912","Other":"#0685cc","Pakistani":"#874245","Other Asian":"#39c2b0","White":"#fdc358", "Total":"#ee7e3b", "White (exclu. Irish)":"#39c2b0","Asian/Asian British":"#7D2248", "Middle Eastern":"#274b57",
	// Religions
	"Any other religion":"#69C2C9","Buddhist":"#C7B200","Christian":"#E55912","Hindu":"#874245","Jewish":"#7D2248","Muslim":"#005776","None":"#fdc358","Sikh":"#69C2C9",
	// Age groups
	"16-17":"#E52E36","18-24":"#F7AB3D","25-49":"#C7B200","50-64":"#005776"
};

export const scales = {
	'Viridis': ColourScale('rgb(122,76,139) 0%, rgb(124,109,168) 12.5%, rgb(115,138,177) 25%, rgb(107,164,178) 37.5%, rgb(104,188,170) 50%, rgb(133,211,146) 62.5%, rgb(189,229,97) 75%, rgb(254,240,65) 87.5%, rgb(254,240,65) 100%'),
	'Heat': ColourScale('rgb(0,0,0) 0%, rgb(128,0,0) 25%, rgb(255,128,0) 50%, rgb(255,255,128) 75%, rgb(255,255,255) 100%'),
	'Planck': ColourScale('rgb(0,0,255) 0%, rgb(0,112,255) 16.666%, rgb(0,221,255) 33.3333%, rgb(255,237,217) 50%, rgb(255,180,0) 66.666%, rgb(255,75,0) 100%'),
	'Plasma': ColourScale('rgb(12,7,134) 0%, rgb(82,1,163) 12.5%, rgb(137,8,165) 25%, rgb(184,50,137) 37.5%, rgb(218,90,104) 50%, rgb(243,135,72) 62.5%, rgb(253,187,43) 75%, rgb(239,248,33) 87.5%'),
	'YFF': ColourScale('rgb(99,190,123) 0%, rgb(250,233,131) 50%, rgb(248,105,107) 100%'),
	'Diverging': ColourScale('rgb(0,87,118) 0%, rgb(247,247,247) 50%, rgb(229,89,18) 100%'),
	'YFF-Highlight': ColourScale('rgba(229,89,18,0) 0%, rgba(229,89,18,1) 100%')
}
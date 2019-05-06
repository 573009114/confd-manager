$(function(){

    this.makeGauge = function(selector, value, color)
    {
	c3.generate({
	    bindto: selector,
	    data: {
		columns: [
		    ['data', value]
		],
		type: 'gauge'
	    },
	    tooltip: {
		show: false
	    },
	    gauge: {
		label: {
		    format: function(value, ratio) {
			return value;
		    },
		    show: false
		},
		min: 0,
		max: 100,
		units: ' %',
		width: 50
	    },
	    color: {
		pattern: [color, color, color], // the 3 color levels for the percentage values.
	    }
	});
    };

    this.makeGauge('#d1-c1', 12, '#1abc9c');
    this.makeGauge('#d1-c2', 22, '#3498db');
    this.makeGauge('#d1-c3', 52, '#f39c12');

});

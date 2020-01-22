import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';
import * as topojson from 'topojson';
import { Router } from '@angular/router';
import { URLS } from 'src/environments/environment';
import { Topology, Objects } from 'topojson-specification';
import { FeatureCollection } from 'geojson';

const COLOR_DIVISION = {
  Atlantic: 'blue',
  Central: 'red',
  Southeast: 'orange',
  Southwest: 'white',
  Northwest: 'yellow',
  Pacific: 'green',
};

export interface City {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  division: string;
}

const R_CIRCLE = 6;


@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit {

  constructor(
    private _router: Router,
  ) { }

  ngOnInit() {
    const projection = d3.geoAlbersUsa().scale(1500).translate([600, 450]);

    const svg = d3.select('div.svg-container')
      .style('position', 'relative')
      .append('svg')
      .attr('width', '100%')
      .attr('height', '100%');

    const path = d3.geoPath()
      .projection(projection);

    const g = svg.append('g');
    g.attr('class', 'map');

    const tooltip = d3.select('body').append('div')
      .attr('class', 'tooltip')
      .style('display', 'none')
      .style('position', 'absolute')
      .style('z-index', '100')
      .style('padding', '0 10px');

    d3.json('assets/usa.json').then((topology: Topology<Objects<{ [name: string]: any; }>>) => {
      const mapFeatures = topojson.feature(topology, topology.objects.states) as FeatureCollection;

      g.selectAll('path')
        .data(mapFeatures.features)
        .enter()
        .append('path')
        .attr('class', 'state')
        .attr('d', path);

      g.append('path')
        .datum(topojson.mesh(topology, topology.objects.states, (a, b) => a !== b))
        .attr('class', 'border')
        .attr('d', path);

      d3.json(URLS.coordinates).then((cities: City[]) => {
        g.selectAll('circle')
          .data(cities)
          .enter()
          .append('circle')
          .attr('cx', d => { const cord: [number, number] = [d.longitude, d.latitude]; return projection(cord)[0]; })
          .attr('cy', d => { const cord: [number, number] = [d.longitude, d.latitude]; return projection(cord)[1]; })
          .attr('r', R_CIRCLE)
          .attr('id', d => {
          return `city-${d.id}`;
          })
          .style('cursor', 'pointer')
          .attr('fill', d => {
            return COLOR_DIVISION[d.division];
          })
          .on('mouseover', d => {
            d3.select(`#city-${d.id}`)
              .attr('r', R_CIRCLE * 2);

            tooltip
              .style('display', 'block')
              .style('background', 'steelblue')
              .text(d.name)
              .style('left', (d3.event.pageX - 40) + 'px')
              .style('top', (d3.event.pageY - 40) + 'px')
              .style('cursor', 'none');
        })
        .on('mouseout', d => {
          d3.select(`#city-${d.id}`)
            .attr('r', R_CIRCLE);

          tooltip
            .style('display', 'none');
        })
        .on('click', d => {
          tooltip.transition()
            .style('display', 'none')
            .duration(0);
          this._router.navigate(['/teams', d.id]);
      });
      });
      });
  }

}

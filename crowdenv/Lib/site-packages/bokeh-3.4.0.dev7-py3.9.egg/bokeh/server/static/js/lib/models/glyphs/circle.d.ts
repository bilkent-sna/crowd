import { XYGlyph, XYGlyphView } from "./xy_glyph";
import type { PointGeometry, SpanGeometry, RectGeometry, PolyGeometry } from "../../core/geometry";
import { LineVector, FillVector, HatchVector } from "../../core/property_mixins";
import type * as visuals from "../../core/visuals";
import type { Rect, Indices } from "../../core/types";
import { RadiusDimension } from "../../core/enums";
import * as p from "../../core/properties";
import type { SpatialIndex } from "../../core/util/spatial";
import type { Context2d } from "../../core/util/canvas";
import { Selection } from "../selections/selection";
export interface CircleView extends Circle.Data {
}
export declare class CircleView extends XYGlyphView {
    model: Circle;
    visuals: Circle.Visuals;
    load_glglyph(): Promise<typeof import("./webgl/circle").CircleGL>;
    protected _index_data(index: SpatialIndex): void;
    protected _map_data(): void;
    protected _mask_data(): Indices;
    protected _render(ctx: Context2d, indices: number[], data?: Partial<Circle.Data>): void;
    protected _hit_point(geometry: PointGeometry): Selection;
    protected _hit_span(geometry: SpanGeometry): Selection;
    protected _hit_rect(geometry: RectGeometry): Selection;
    protected _hit_poly(geometry: PolyGeometry): Selection;
    draw_legend_for_index(ctx: Context2d, { x0, y0, x1, y1 }: Rect, index: number): void;
}
export declare namespace Circle {
    type Attrs = p.AttrsOf<Props>;
    type Props = XYGlyph.Props & {
        radius: p.DistanceSpec;
        radius_dimension: p.Property<RadiusDimension>;
        hit_dilation: p.Property<number>;
    } & Mixins;
    type Mixins = LineVector & FillVector & HatchVector;
    type Visuals = XYGlyph.Visuals & {
        line: visuals.LineVector;
        fill: visuals.FillVector;
        hatch: visuals.HatchVector;
    };
    type Data = p.GlyphDataOf<Props>;
}
export interface Circle extends Circle.Attrs {
}
export declare class Circle extends XYGlyph {
    properties: Circle.Props;
    __view_type__: CircleView;
    constructor(attrs?: Partial<Circle.Attrs>);
}
//# sourceMappingURL=circle.d.ts.map
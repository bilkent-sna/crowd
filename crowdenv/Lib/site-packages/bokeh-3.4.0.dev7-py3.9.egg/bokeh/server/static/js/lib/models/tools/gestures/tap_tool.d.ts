import { SelectTool, SelectToolView } from "./select_tool";
import type { CallbackLike1 } from "../../../core/util/callbacks";
import type * as p from "../../../core/properties";
import type { TapEvent, KeyModifiers } from "../../../core/ui_events";
import type { PointGeometry } from "../../../core/geometry";
import type { SelectionMode } from "../../../core/enums";
import { TapBehavior, TapGesture } from "../../../core/enums";
import type { ColumnarDataSource } from "../../sources/columnar_data_source";
import type { DataRendererView } from "../../renderers/data_renderer";
export declare const Modifiers: import("../../../core/kinds").Kinds.Or<[Partial<{
    shift: boolean;
    ctrl: boolean;
    alt: boolean;
}>, Map<"shift" | "ctrl" | "alt", boolean>]>;
export type Modifiers = typeof Modifiers["__type__"];
export type TapToolCallback = CallbackLike1<TapTool, {
    geometries: PointGeometry & {
        x: number;
        y: number;
    };
    source: ColumnarDataSource;
    event: {
        modifiers?: KeyModifiers;
    };
}>;
export declare class TapToolView extends SelectToolView {
    model: TapTool;
    _tap(ev: TapEvent): void;
    _doubletap(ev: TapEvent): void;
    _handle_tap(ev: TapEvent): void;
    protected _select(geometry: PointGeometry, final: boolean, mode: SelectionMode): void;
    protected _inspect(geometry: PointGeometry, modifiers?: KeyModifiers): void;
    protected _emit_callback(rv: DataRendererView, geometry: PointGeometry, source: ColumnarDataSource, modifiers?: KeyModifiers): void;
}
export declare namespace TapTool {
    type Attrs = p.AttrsOf<Props>;
    type Props = SelectTool.Props & {
        behavior: p.Property<TapBehavior>;
        gesture: p.Property<TapGesture>;
        modifiers: p.Property<Modifiers>;
        callback: p.Property<TapToolCallback | null>;
    };
}
export interface TapTool extends TapTool.Attrs {
}
export declare class TapTool extends SelectTool {
    properties: TapTool.Props;
    __view_type__: TapToolView;
    constructor(attrs?: Partial<TapTool.Attrs>);
    tool_name: string;
    tool_icon: string;
    event_type: "tap";
    default_order: number;
}
//# sourceMappingURL=tap_tool.d.ts.map
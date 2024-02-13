import type { StyleSheetLike } from "../../core/dom";
import type { ViewStorage, IterViews } from "../../core/build_views";
import type * as p from "../../core/properties";
import { UIElement, UIElementView } from "../ui/ui_element";
import { Logo, Location } from "../../core/enums";
import { Tool } from "./tool";
import type { ToolLike } from "./tool_proxy";
import { ToolProxy } from "./tool_proxy";
import { ToolButton } from "./tool_button";
import { GestureTool } from "./gestures/gesture_tool";
import { InspectTool } from "./inspectors/inspect_tool";
import { ActionTool } from "./actions/action_tool";
import { HelpTool } from "./actions/help_tool";
import { ContextMenu } from "../../core/util/menus";
export declare class ToolbarView extends UIElementView {
    model: Toolbar;
    protected readonly _tool_button_views: ViewStorage<ToolButton>;
    protected _tool_buttons: ToolButton[][];
    protected _items: HTMLElement[];
    get tool_buttons(): ToolButton[];
    protected _overflow_menu: ContextMenu;
    protected _overflow_el: HTMLElement;
    get overflow_el(): HTMLElement;
    private _visible;
    get visible(): boolean;
    children(): IterViews;
    has_finished(): boolean;
    initialize(): void;
    lazy_initialize(): Promise<void>;
    connect_signals(): void;
    stylesheets(): StyleSheetLike[];
    remove(): void;
    protected _build_tool_button_views(): Promise<void>;
    set_visibility(visible: boolean): void;
    protected _on_visible_change(): void;
    _after_resize(): void;
    render(): void;
    _after_render(): void;
}
declare const GesturesMap: import("../../core/kinds").Kinds.Struct<{
    pan: {
        tools: any;
        active: any;
    };
    scroll: {
        tools: any;
        active: any;
    };
    pinch: {
        tools: any;
        active: any;
    };
    rotate: {
        tools: any;
        active: any;
    };
    move: {
        tools: any;
        active: any;
    };
    tap: {
        tools: any;
        active: any;
    };
    doubletap: {
        tools: any;
        active: any;
    };
    press: {
        tools: any;
        active: any;
    };
    pressup: {
        tools: any;
        active: any;
    };
    multi: {
        tools: any;
        active: any;
    };
}>;
type GesturesMap = typeof GesturesMap["__type__"];
export type Drag = Tool;
export declare const Drag: typeof Tool;
export type Inspection = Tool;
export declare const Inspection: typeof Tool;
export type Scroll = Tool;
export declare const Scroll: typeof Tool;
export type Tap = Tool;
export declare const Tap: typeof Tool;
type ActiveGestureToolsProps = {
    active_drag: p.Property<ToolLike<Drag> | "auto" | null>;
    active_scroll: p.Property<ToolLike<Scroll> | "auto" | null>;
    active_tap: p.Property<ToolLike<Tap> | "auto" | null>;
    active_multi: p.Property<ToolLike<GestureTool> | "auto" | null>;
};
export declare namespace Toolbar {
    type Attrs = p.AttrsOf<Props>;
    type Props = UIElement.Props & {
        tools: p.Property<(Tool | ToolProxy<Tool>)[]>;
        logo: p.Property<Logo | null>;
        autohide: p.Property<boolean>;
        buttons: p.Property<(ToolButton | null)[] | "auto">;
        location: p.Property<Location>;
        inner: p.Property<boolean>;
        gestures: p.Property<GesturesMap>;
        actions: p.Property<ToolLike<ActionTool>[]>;
        inspectors: p.Property<ToolLike<InspectTool>[]>;
        help: p.Property<ToolLike<HelpTool>[]>;
        auxiliaries: p.Property<ToolLike<Tool>[]>;
    } & ActiveGestureToolsProps & {
        active_inspect: p.Property<ToolLike<Inspection> | ToolLike<Inspection>[] | "auto" | null>;
    };
}
export interface Toolbar extends Toolbar.Attrs {
}
export declare class Toolbar extends UIElement {
    properties: Toolbar.Props;
    __view_type__: ToolbarView;
    constructor(attrs?: Partial<Toolbar.Attrs>);
    get horizontal(): boolean;
    get vertical(): boolean;
    connect_signals(): void;
    initialize(): void;
    protected _init_tools(): void;
    protected _activate_tools(): void;
    _active_change(tool: ToolLike<GestureTool>): void;
}
export {};
//# sourceMappingURL=toolbar.d.ts.map
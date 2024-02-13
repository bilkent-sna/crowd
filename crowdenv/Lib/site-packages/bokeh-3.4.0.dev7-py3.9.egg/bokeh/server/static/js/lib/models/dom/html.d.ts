import { DOMNode, DOMNodeView } from "./dom_node";
import { UIElement } from "../ui/ui_element";
import type { ViewStorage, IterViews } from "../../core/build_views";
import type * as p from "../../core/properties";
declare const HTMLRef: import("../../core/kinds").Kinds.Or<[DOMNode, UIElement]>;
type HTMLRef = typeof HTMLRef["__type__"];
declare const RawHTML: import("../../core/kinds").Kinds.String;
type RawHTML = typeof RawHTML["__type__"];
export declare class HTMLView extends DOMNodeView {
    model: HTML;
    el: HTMLElement;
    protected readonly _refs: ViewStorage<HTMLRef>;
    get refs(): HTMLRef[];
    children(): IterViews;
    lazy_initialize(): Promise<void>;
    remove(): void;
    render(): void;
    parse_html(html: string): Node[];
}
export declare namespace HTML {
    type Attrs = p.AttrsOf<Props>;
    type Props = DOMNode.Props & {
        html: p.Property<RawHTML | (RawHTML | HTMLRef)[]>;
        refs: p.Property<HTMLRef[]>;
    };
}
export interface HTML extends HTML.Attrs {
}
export declare class HTML extends DOMNode {
    properties: HTML.Props;
    __view_type__: HTMLView;
    constructor(attrs?: Partial<HTML.Attrs>);
}
export {};
//# sourceMappingURL=html.d.ts.map
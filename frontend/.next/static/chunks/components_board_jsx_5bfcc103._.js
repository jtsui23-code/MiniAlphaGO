(globalThis.TURBOPACK = globalThis.TURBOPACK || []).push([typeof document === "object" ? document.currentScript : undefined, {

"[project]/components/board.jsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { g: global, __dirname, k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "default": (()=>GoBoard)
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
'use client';
;
const BOARD_SIZE = 19;
const CELL_SIZE = 30;
const STONE_RADIUS = 10;
function GoBoard() {
    _s();
    const [board, setBoard] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(Array.from({
        length: BOARD_SIZE
    }, {
        "GoBoard.useState": ()=>Array(BOARD_SIZE).fill(null)
    }["GoBoard.useState"]));
    const [currentPlayer, setCurrentPlayer] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])('black');
    const handleClick = (x, y)=>{
        if (board[y][x]) return;
        const newBoard = board.map((row, j)=>row.map((cell, i)=>i === x && j === y ? currentPlayer : cell));
        setBoard(newBoard);
        setCurrentPlayer(currentPlayer === 'black' ? 'white' : 'black');
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("svg", {
        width: CELL_SIZE * (BOARD_SIZE - 1),
        height: CELL_SIZE * (BOARD_SIZE - 1),
        style: {
            backgroundColor: '#deb887',
            display: 'block'
        },
        children: [
            Array.from({
                length: BOARD_SIZE
            }).map((_, i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("line", {
                            x1: i * CELL_SIZE,
                            y1: 0,
                            x2: i * CELL_SIZE,
                            y2: (BOARD_SIZE - 1) * CELL_SIZE,
                            stroke: "black"
                        }, `v-${i}`, false, {
                            fileName: "[project]/components/board.jsx",
                            lineNumber: 34,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("line", {
                            x1: 0,
                            y1: i * CELL_SIZE,
                            x2: (BOARD_SIZE - 1) * CELL_SIZE,
                            y2: i * CELL_SIZE,
                            stroke: "black"
                        }, `h-${i}`, false, {
                            fileName: "[project]/components/board.jsx",
                            lineNumber: 42,
                            columnNumber: 11
                        }, this)
                    ]
                }, void 0, true)),
            board.map((row, y)=>row.map((cell, x)=>cell ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("circle", {
                        cx: x * CELL_SIZE,
                        cy: y * CELL_SIZE,
                        r: STONE_RADIUS,
                        fill: cell,
                        stroke: "black"
                    }, `${x}-${y}`, false, {
                        fileName: "[project]/components/board.jsx",
                        lineNumber: 57,
                        columnNumber: 13
                    }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("circle", {
                        cx: x * CELL_SIZE,
                        cy: y * CELL_SIZE,
                        r: CELL_SIZE / 2,
                        fill: "transparent",
                        onClick: ()=>handleClick(x, y)
                    }, `${x}-${y}-click`, false, {
                        fileName: "[project]/components/board.jsx",
                        lineNumber: 66,
                        columnNumber: 13
                    }, this)))
        ]
    }, void 0, true, {
        fileName: "[project]/components/board.jsx",
        lineNumber: 26,
        columnNumber: 5
    }, this);
}
_s(GoBoard, "Yx4atKbOJ4mWAXytNkxjGXDCnLo=");
_c = GoBoard;
var _c;
__turbopack_context__.k.register(_c, "GoBoard");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
}]);

//# sourceMappingURL=components_board_jsx_5bfcc103._.js.map
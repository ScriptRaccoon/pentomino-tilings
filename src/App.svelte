<script lang="ts">
	type coord = [number, number]
	type tiling = Record<string, Array<coord>>
	let tilings: Array<tiling>
	let names: Array<string>
	let current_index = 0
	$: current_tiling = tilings?.[current_index]

	const n = 3
	const m = 20

	const COLORS = {
		F: "rgb(255, 0, 0)",
		I: "rgb(255, 128, 0)",
		L: "rgb(255, 255, 0)",
		N: "rgb(128, 255, 0)",
		P: "rgb(0, 255, 0)",
		T: "rgb(0, 255, 128)",
		U: "rgb(0, 255, 255)",
		V: "rgb(0, 128, 255)",
		W: "rgb(0, 0, 255)",
		X: "rgb(128, 0, 255)",
		Y: "rgb(255, 0, 255)",
		Z: "rgb(255, 0, 128)",
	} as Record<string, string>

	async function init() {
		const res = await fetch("/data/tilings-3-20.json")
		if (res.ok) {
			tilings = (await res.json()) as Array<tiling>
			names = Object.keys(tilings[0] ?? {})
		}
	}

	init()

	function go_left() {
		current_index--
		if (current_index < 0) {
			current_index = tilings.length - 1
		}
	}

	function go_right() {
		current_index += 1
		if (current_index >= tilings.length) {
			current_index = 0
		}
	}
</script>

<h1>Pentomino Tilings</h1>

<menu>
	<button on:click={go_left}> Left </button>
	<button on:click={go_right}> Right </button>
</menu>

<p>
	Tiling #{current_index + 1}
</p>

{#if names && current_tiling}
	<div class="board" style:--n={n} style:--m={m}>
		{#each names as name}
			{#each { length: 5 } as _, index}
				{@const [y, x] = current_tiling[name][index]}
				<div
					class="cell"
					style:--x={x}
					style:--y={y}
					style:--color={COLORS[name]}
				/>
			{/each}
		{/each}
	</div>
{/if}

<style>
	.board {
		--u: 3rem;
		position: relative;
		height: calc(var(--n) * var(--u));
		width: calc(var(--m) * var(--u));
	}

	.cell {
		background-color: var(--color);
		width: var(--u);
		height: var(--u);
		left: calc(var(--x) * var(--u));
		top: calc(var(--y) * var(--u));
		border: 1px solid gray;
		position: absolute;
	}
</style>

<script lang="ts">
	import { onMount } from "svelte"
	import { COLORS, SIZES } from "./config"
	import { get_tilings, type tiling } from "./tilings"

	let tilings: Array<tiling>
	let names: Array<string>

	let current_index = 0
	$: current_tiling = tilings?.[current_index]

	let selected_n = 3
	let n = 3
	let m = 20

	let loading = false

	async function init() {
		const new_n = selected_n
		const new_m = new_n != 8 ? Math.floor(60 / new_n) : 8

		loading = true
		const new_tilings = await get_tilings(new_n, new_m)

		if (new_tilings) {
			tilings = new_tilings
			current_index = 0
			n = new_n
			m = new_m
		} else {
			window.alert("Could not retrieve the data at this moment")
		}

		if (!names) names = Object.keys(tilings[0] ?? {})

		loading = false
	}

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

	onMount(init)
</script>

<header>
	<h1>Pentomino Tilings</h1>
</header>

<main>
	{#if names && current_tiling}
		<h2 class="counter" aria-live="polite">
			Tiling #{current_index + 1} / {tilings.length}
		</h2>
		<div class="board" style:--n={n} style:--m={m}>
			{#each names as name}
				{#each { length: 5 } as _, index}
					{@const [y, x] = current_tiling[name][index]}
					<div
						class="square"
						style:--x={x}
						style:--y={y}
						style:--color={COLORS[name]}
					/>
				{/each}
			{/each}
		</div>
	{/if}

	<menu>
		<div>
			<button
				disabled={!current_tiling}
				on:click={go_left}
				aria-label="previous"
			>
				<img
					src="arrow.svg"
					alt="arrow left"
					aria-hidden="true"
				/>
			</button>
			<button
				disabled={!current_tiling}
				on:click={go_right}
				aria-label="next"
			>
				<img
					class="flipped"
					src="arrow.svg"
					alt="arrow right"
					aria-hidden="true"
				/>
			</button>
		</div>

		<div>
			<label for="size">Size</label>
			<select
				id="size"
				bind:value={selected_n}
				on:change={init}
				disabled={loading}
			>
				{#each SIZES as [x, y]}
					<option value={x}>{x} &times; {y}</option>
				{/each}
			</select>
		</div>
	</menu>

	{#if loading}
		<div>Loading...</div>
	{/if}
</main>

<style>
	header {
		padding-block: 2rem;
	}

	h1 {
		line-height: 1.1;
	}

	menu {
		margin-block: 1rem;
		display: flex;
		gap: 1.5rem;
		flex-direction: row-reverse;
		flex-wrap: wrap;
	}

	menu div {
		display: flex;
		gap: 0.5rem;
	}

	.counter {
		font-size: 1.25rem;
		font-weight: initial;
		margin-bottom: 0.5rem;
	}

	.board {
		--u: min(5rem, calc((100vw - 2rem) / var(--m)));
		position: relative;
		height: calc(var(--n) * var(--u));
		width: calc(var(--m) * var(--u));
	}

	.square {
		background-color: var(--color);
		width: var(--u);
		height: var(--u);
		left: calc(var(--x) * var(--u));
		top: calc(var(--y) * var(--u));
		border: 1px solid var(--bg);
		position: absolute;
		transition: 750ms ease;
	}

	button {
		opacity: 0.75;
	}

	button:hover,
	button:focus-visible {
		opacity: 1;
	}

	@media (min-width: 42rem) {
		h1 {
			font-size: 3rem;
		}
		menu {
			flex-direction: row;
		}
	}
</style>

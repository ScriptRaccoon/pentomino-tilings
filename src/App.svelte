<script lang="ts">
	import { onMount } from "svelte"
	import { COLORS } from "./config"

	type coord = [number, number]
	type tiling = Record<string, Array<coord>>

	let tilings: Array<tiling>
	let names: Array<string>

	let current_index = 0
	$: current_tiling = tilings?.[current_index]

	let selection = "3"
	let n = 3
	let m = 20

	let loading = false

	function update_selection() {
		n = parseInt(selection)
		m = Math.floor(60 / n)
		init()
	}

	async function init() {
		loading = true
		const path = `/data/tilings-${n}-${m}.json`
		const res = await fetch(path)
		if (res.ok) {
			tilings = (await res.json()) as Array<tiling>
			names = Object.keys(tilings[0] ?? {})
			current_index = 0
		} else {
			window.alert("Could not retrieve the data at this moment")
		}
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

<h1>Pentomino Tilings</h1>

<menu>
	<button disabled={!current_tiling} on:click={go_left}>
		Left
	</button>
	<button disabled={!current_tiling} on:click={go_right}>
		Right
	</button>
	<label for="size">Size</label>
	<select
		id="size"
		bind:value={selection}
		on:change={update_selection}
	>
		<option value="3">3 &times; 20</option>
		<option value="4">4 &times; 15</option>
		<option value="5">5 &times; 12</option>
		<option value="6">6 &times; 10</option>
	</select>
</menu>

{#if current_tiling}
	<p>
		Tiling #{current_index + 1}
	</p>
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

{#if loading}
	<div>Loading...</div>
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

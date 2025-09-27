import time
import argparse
from sokoban import Map
from search_methods.solver import Solver
from sokoban.gif import save_images, create_gif

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("algorithm", choices=["lrta*", "beam-search"])
    parser.add_argument("map_file")
    args = parser.parse_args()

    crt_map = Map.from_yaml(args.map_file)

    start_time = time.time()
    algo = Solver(crt_map, algorithm=args.algorithm)
    path = algo.solve()
    end_time = time.time()
    elapsed_time = end_time - start_time

    images_folder = "temp_frames"
    gif_name = f"{args.algorithm}_solution"
    gif_output_folder = "gifs"
    save_images(path, images_folder)
    create_gif(images_folder, gif_name, gif_output_folder)

    final_state = path[-1]
    num_pulls = final_state.undo_moves
    total_states = final_state.explored_states

    print(f"Numar stari explorate: {total_states}")
    print(f"Numar total de pull-uri: {num_pulls}")
    print(f"Timp total de rulare: {elapsed_time:.4f} secunde")

if __name__ == '__main__':
    main()

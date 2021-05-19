# ompl_demo

## Usage

```bash
python3 src/ompl_demo.py --help
usage: ompl_demo.py [-h] [--start START [START ...]] --goal GOAL [GOAL ...]
                    [--output_file_path OUTPUT_FILE_PATH]
                    [--env_mesh_path ENV_MESH_PATH]
                    [--robot_mesh_path ROBOT_MESH_PATH]

OMPL demo

optional arguments:
  -h, --help            show this help message and exit
  --start START [START ...]
                        Start point in a format `lat, lon, alt`
  --goal GOAL [GOAL ...]
                        Goal point in a format `lat, lon, alt`
  --output_file_path OUTPUT_FILE_PATH
                        Path to a .txt file for further visualization
  --env_mesh_path ENV_MESH_PATH
                        Path to environement .dae file
  --robot_mesh_path ROBOT_MESH_PATH
                        Path to robot .dae file
```
## Example

```bash
python3 src/ompl_demo.py \
    --goal -83.77534490949962 -55.690830378508565 2403.460302218876
```

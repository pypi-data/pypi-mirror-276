import torch
import os
from vbench2_beta_long import VBenchLong
from datetime import datetime
import argparse
import json

def parse_args():

    CUR_DIR = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description='VBench', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "--output_path",
        type=str,
        default='./evaluation_results/',
        help="output path to save the evaluation results",
    )
    parser.add_argument(
        "--full_json_dir",
        type=str,
        default=f'{CUR_DIR}/vbench/VBench_full_info.json',
        help="path to save the json file that contains the prompt and dimension information",
    )
    parser.add_argument(
        "--videos_path",
        type=str,
        required=True,
        help="folder that contains the sampled videos",
    )
    parser.add_argument(
        "--dimension",
        nargs='+',
        required=True,
        help="list of evaluation dimensions, usage: --dimension <dim_1> <dim_2>",
    )
    parser.add_argument(
        "--load_ckpt_from_local",
        type=bool,
        required=False,
        help="whether load checkpoints from local default paths (assuming you have downloaded the checkpoints locally",
    )
    parser.add_argument(
        "--read_frame",
        type=bool,
        required=False,
        help="whether directly read frames, or directly read videos",
    )
    parser.add_argument(
        "--mode",
        choices=['custom_input', 'vbench_standard', 'vbench_category', 'long_vbench_standard', 'long_custom_input'],
        default='vbench_standard',
        help="""This flags determine the mode of evaluations, choose one of the following:
        1. "custom_input": receive input prompt from either --prompt/--prompt_file flags or the filename
        2. "vbench_standard": evaluate on standard prompt suite of VBench
        3. "vbench_category": evaluate on specific category
        """,
    )
    parser.add_argument(
        "--custom_input",
        action="store_true",
        required=False,
        help="(deprecated) use --mode=\"custom_input\" instead",
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="",
        help="""Specify the input prompt
        If not specified, filenames will be used as input prompts
        * Mutually exclusive to --prompt_file.
        ** This option must be used with --custom_input flag
        """
    )
    parser.add_argument(
        "--prompt_file",
        type=str,
        required=False,
        help="""Specify the path of the file that contains prompt lists
        If not specified, filenames will be used as input prompts
        * Mutually exclusive to --prompt.
        ** This option must be used with --custom_input flag
        """
    )
    parser.add_argument(
        "--category",
        type=str,
        required=False,
        help="""This is for mode=='vbench_category'
        The category to evaluate on, usage: --category=animal.
        """,
    )

    ## for dimension specific params ###
    parser.add_argument(
        "--imaging_quality_preprocessing_mode",
        type=str,
        required=False,
        default='longer',
        help="""This is for setting preprocessing in imaging_quality
        1. 'shorter': if the shorter side is more than 512, the image is resized so that the shorter side is 512.
        2. 'longer': if the longer side is more than 512, the image is resized so that the longer side is 512.
        3. 'shorter_centercrop': if the shorter side is more than 512, the image is resized so that the shorter side is 512. 
        Then the center 512 x 512 after resized is used for evaluation.
        4. 'None': no preprocessing
        """,
    )


    parser.add_argument(
        "--use_semantic_splitting",
        action="store_true",
        required=False,
        help="""Whether to use semantic splitting tools
        """,
    )

    # for dreamsim & other models
    parser.add_argument(
        "--feature_extractor",
        type=str,
        default='vbench',
        choices=['vbench', 'dreamsim'],
        help="""This will select the model to caculate 
        consistency dimension's scores.
        """,
    )
    parser.add_argument(
        "--w_inclip",
        type=float,
        default=1.0,
        help="""Weight for in-clip scores, consistency dimensions
        """,
    )
    parser.add_argument(
        "--w_clip2clip",
        type=float,
        default=0.0,
        help="""Weight for clip-clip scores, consistency dimensions
        """,
    )
    # for mixture clip length
    parser.add_argument(
        "--clip_length_config",
        type=str,
        default='clip_length_mix.yaml',
        help="""Config files for different clip length.
        """,
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    print(f'args: {args}')

    device = torch.device("cuda")
    my_VBench = VBenchLong(device, args.full_json_dir, args.output_path)
    
    print(f'start evaluation')

    current_time = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

    kwargs = {}

    prompt = []

    assert args.custom_input == False, "(Deprecated) use --mode=custom_input instead"
    
    if (args.prompt_file is not None) and (args.prompt != ""):
        raise Exception("--prompt_file and --prompt cannot be used together")
    if (args.prompt_file is not None or args.prompt != "") and (not args.mode=='custom_input'):
        raise Exception("must set --mode=custom_input for using external prompt")

    if args.prompt_file:
        with open(args.prompt_file, 'r') as f:
            prompt = json.load(f)
        assert type(prompt) == dict, "Invalid prompt file format. The correct format is {\"video_path\": prompt, ... }"
    elif args.prompt != "":
        prompt = [args.prompt]

    if args.category != "":
        kwargs['category'] = args.category


    kwargs['feature_extractor'] = args.feature_extractor
    kwargs['imaging_quality_preprocessing_mode'] = args.imaging_quality_preprocessing_mode
    kwargs['clip_length_config'] = args.clip_length_config
    kwargs['w_inclip'] = args.w_inclip
    kwargs['w_clip2clip'] = args.w_clip2clip
    kwargs['use_semantic_splitting'] = args.use_semantic_splitting

    my_VBench.evaluate(
        videos_path = args.videos_path,
        name = f'results_{current_time}',
        prompt_list=prompt, # pass in [] to read prompt from filename
        dimension_list = args.dimension,
        local=args.load_ckpt_from_local,
        read_frame=args.read_frame,
        mode=args.mode,
        **kwargs
    )
    print('done')


if __name__ == "__main__":
    main()

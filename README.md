# HomeVal

This repo stores the code necessary to generate experimental reports
explaining how the CCAO Data team's residential model valued any particular
single-family home or multifamily home with six or fewer units.

## Development

### Running a development server

This project expects that you have the [Hugo CLI](https://gohugo.io/installation/)
installed on your machine.

> [!NOTE]
> While the Data team often does work on the server, you should do Hugo
> development on your laptop in order to run the development site. Hugo
> installation is easiest using WSL, where you can install it by running
> `sudo snap install hugo` and entering your WSL user password. Your WSL
> password will most likely be different from your laptop password; if
> you're having trouble authenticating, reach out to a senior staff member
> for help.

1. Ensure that Hugo is installed correctly by running `hugo version`.
2. Navigate to the `hugo/` subdirectory and run the development server:

```
cd hugo
hugo serve
```

3. Any reports that [you have generated](#generating-reports)
   will be available in a browser at http://localhost:1313/.

### Generating reports

You can use the [`generate_homeval`
script](https://github.com/ccao-data/homeval/blob/main/scripts/generate_homeval/generate_homeval.py)
to generate reports that you can view locally.

Start by creating a virtual environment for the script and installing its
dependencies:

```
uv venv scripts/generate_homeval/.venv
source scripts/generate_homeval/.venv/bin/activate
uv pip install scripts/generate_homeval
```

Then, use the script to generate reports for one or more PINs using a given
comps run ID:

```
AWS_ATHENA_S3_STAGING_DIR="<your_athena_staging_dir>" python3 scripts/generate_homeval/generate_homeval.py \
   --run-id <your_comps_run_id> \
   --pin <one_or_more_space_separated_pins>
```

Run `python3 scripts/generate_homeval/generate_homeval.py --help` to see full
documentation for the script.

## Deployment

We manage deployments using the [`generate-homeval` GitHub
workflow](https://github.com/ccao-data/homeval/actions/workflows/generate-homeval.yaml).
That workflow includes options for deploying to a development environment as
well as the production environment.

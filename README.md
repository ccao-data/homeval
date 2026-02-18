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

### Deploying a new model run

During modeling season, we often deploy non-final model runs to the staging app
in order to QC the pipeline before we deploy to prod. We also perform
one final deployment to the prod app once we've finalized the model. These
updates can be tricky, since they require strategically building certain dbt
resources in the [`data-architecture`
repo](https://github.com/ccao-data/data-architecture/) in the correct order.

See the sections below for detailed instructions on how to perform these
deployments, with slightly different steps for staging and prod.

#### Deploying to staging for a new, non-final model run

1. Create a new branch in `data-architecture` to deploy staging versions of the
   dbt models that HomeVal depends on for its data
2. Update the `pinval.model_run` seed with the non-final model runs to use as
   the basis for cards, comps, and SHAPs
3. Update the `model.final_model_raw` seed with the non-final model run that
   you used for the `card` type in step 2
4. Update the `pinval.comp` dbt model so that the `WHERE` filter in the
   `training_data` subquery includes the non-final model run that you added to
   `model.final_model_raw` in step 3
5. Commit your changes to your branch, push it, and open a PR
   - Your PR will trigger a `build-and-run-dbt` workflow to build staging
     resources. This build will fail, since not all of the necessary precursor
     resources will exist yet. Ignore this failure and move on to the next step
6. Trigger a [`build-and-test-dbt`
   workflow](https://github.com/ccao-data/data-architecture/actions/workflows/build_and_test_dbt.yaml)
   using your branch to build necessary HomeVal resources in the right order.
   Use the following value for the input box labeled
   "A space-separated list of dbt models",
      - `model.final_model model.training_data pinval.assessment_card pinval.comp`
7. Create a new branch in this repo to deploy a staging version of the site
8. Take note of the schemas that dbt used to create your staging resources
   in the workflow logs from step 5 above, and edit
   `scripts/generate_homeval/constants.py` in this repo to point to the staging
   versions of the core HomeVal tables. Core HomeVal tables include:
      - `HOMEVAL_ASSESSMENT_CARD_TABLE`
      - `HOMEVAL_COMP_TABLE`
9. Kick off a [`generate-homeval` workflow
   run](https://github.com/ccao-data/homeval/actions/workflows/generate-homeval.yaml)
   using the following parameters:
   - "Use workflow from": Select your branch name
   - "Assessment year": The assessment year for the new model run that you
     would like to use as the basis for your staging deployment
   - "Environment": "Development bucket"
   - "Build reports by neighborhood": Check the box
   - "Only generate reports for PINs that are eligible for reports": You can
     leave this either checked or unchecked, depending on whether you want
     to generate verbose error pages; for staging deployments, verbose error
     pages are usually not necessary
   - Leave all other fields either blank or unchecked

#### Deploying to prod for a new, final model run

1. Follow steps 1-6 in the instructions above for deploying to staging
2. Seek approval on your `data-architecture` PR, merge it in, and wait for
   the `build-and-test-dbt` workflow to rebuild prod resources
3. Once dbt has rebuilt `pinval.comp` and `pinval.assessment_card` using the
   new model run, kick off a [`generate-homeval` workflow
   run](https://github.com/ccao-data/homeval/actions/workflows/generate-homeval.yaml)
   using the following parameters:
   - "Use workflow from": "main"
   - "Assessment year": The assessment year for the new model run that you
     would like to use as the basis for your staging deployment
   - "Environment": "Production bucket"
   - "Build reports by neighborhood": Check the box
   - Leave all other fields either blank or unchecked

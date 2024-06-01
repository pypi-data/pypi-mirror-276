# Remaining TODO

General:
* notes scattered in comments and docstrings (sorry!)
* Docker-ification. (there should be existing images for SeqRepo and UTA, not sure how up-to-date they are).
* Add extra stuff that appears in mapping JSON objects (``vrs_ref_allele_seq``).
* Currently using VRS 2.0a-based libraries. For lifting back to VRS 1.3, some basic post-processing should be fine (annoying but shouldn't be too trivial)
* Without access to a production DynamoDB instance, Gene Normalizer will be quickest and easiest to set up via a PostgreSQL data backend (https://gene-normalizer.readthedocs.io/en/latest/install.html#quick-installation). That, however, requires an extra dependency group (noted in README). We might want to make a `pg` dependency group here or just include it in core dependencies. 
* On that note, I've only done minimal testing of how possible it would be to drop the gene normalizer dependency entirely, but it'd be nice to get there.
* Pickle files for most of the checkpoint objects are available here: https://mavedb-mapping.s3.us-east-2.amazonaws.com/dcd_mapping_pickles.zip

Alignment:
* Pretty sure this is mostly done.
* Need to sufficiently mock/patch things in tests

Transcript selection:
* IndexError in calculating offset on lots of new (2023) scoresets.
* Tests will need some extensive mocking (or cassettes?) for reliance on UTA and other external dependencies
* Some discrepancies between original mappings and the output of this pipeline with respect to transcripts being tagged as `MANE Select` vs `MANE Plus Clinical`, as mentioned on the call. We haven't exhaustively determined scope of this but Jeremy Arbesfeld can help if there are further questions about this.

VRS mapping:
* In general, this stuff is still pretty rough. Not passing informal tests, and needs formal tests.
* Finish double-checking the SeqRepo storage workaround
* A fair amount of small questions about conditions written to handle specific scoresets/edge cases
* Can be ready for CI by manually patching the SequenceStore class (or using SeqRepoRESTDataProxy and cassettes).

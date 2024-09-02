commit_comment_event_df = commit_comment_event_df.select("event_id","type", "actor_id", "org_id","repo_id","public", "created_at", col("payload.action").alias("action"))
# commit_comment_event_df = spark.createDataFrame(commit_comment_event_df.rdd, schema=event_schema_with_action)

sponsorship_event_df = sponsorship_event_df.select("event_id","type", "actor_id", "org_id","repo_id","public", "created_at", col("payload.action").alias("action"))
# sponsorship_event_df = spark.createDataFrame(sponsorship_event_df.rdd, schema=event_schema_with_action)

create_event_df = create_event_df.select("event_id","type", "actor_id", "org_id","repo_id","public", "created_at", col("payload.ref_type").alias("ref_type"))
# create_event_df = spark.createDataFrame(create_event_df.rdd, schema=event_schema_with_ref_type)

delete_event_df = delete_event_df.select("event_id","type", "actor_id", "org_id","repo_id","public", "created_at", col("payload.ref_type").alias("ref_type"))
# delete_event_df = spark.createDataFrame(delete_event_df.rdd, schema=event_schema_with_ref_type)

fork_event_df = fork_event_df.select("event_id","type", "actor_id", "org_id","repo_id","public", "created_at")
# fork_event_df = spark.createDataFrame(fork_event_df.rdd, schema=event_schema_basic)

push_event_df = push_event_df.select("event_id","type", "actor_id", "org_id","repo_id","public", "created_at", col("payload.size").cast(IntegerType()).alias("num_commits"), col("payload.ref").alias("payload_ref"), col("payload.commits.author.email").alias("author_email"), col("payload.commits.author.name").alias("author_name"), col("payload.commits.message").alias("message"))
# push_event_df = spark.createDataFrame(push_event_df.rdd, schema=push_event_schema)

pull_request_review_thread_event_df = pull_request_review_thread_event_df.select("event_id","type", "actor_id", "org_id","repo_id","public", "created_at", col("payload.action").alias("action"))
# pull_request_review_thread_event = spark.createDataFrame(pull_request_review_thread_event_df.rdd, schema=event_schema_with_action)

pull_request_review_comment_event_df = pull_request_review_comment_event_df.select("event_id","type", "actor_id", "org_id","repo_id","public", "created_at", col("payload.action").alias("action"))
# pull_request_review_comment_event = spark.createDataFrame(pull_request_review_comment_event_df.rdd, schema=event_schema_with_action)

pull_request_review_event_df = pull_request_review_event_df.select("event_id","type", "actor_id", "org_id","repo_id","public", "created_at", col("payload.action").alias("action"))
# pull_request_review_event = spark.createDataFrame(pull_request_review_event_df.rdd, schema=event_schema_with_action)

pull_request_event_df = pull_request_event_df.select("event_id","type", "actor_id", "org_id","repo_id","public", "created_at", col("payload.action").alias("action"))
# pull_request_event = spark.createDataFrame(pull_request_event_df.rdd, schema=event_schema_with_action)

gollum_event_df = gollum_event_df.select("event_id","type", "actor_id", "org_id","repo_id","public", "created_at")
# gollum_event_df = spark.createDataFrame(gollum_event_df.rdd, schema=event_schema_basic)

issue_comment_event_df = issue_comment_event_df.select("event_id","type", "actor_id", "org_id","repo_id","public", "created_at", col("payload.action").alias("action"))
# issue_comment_event_df = spark.createDataFrame(issue_comment_event_df.rdd, schema=event_schema_with_action)

issues_event_df = issues_event_df.select("event_id","type", "actor_id", "org_id","repo_id","public", "created_at", col("payload.action").alias("action"))
# issues_event_df = spark.createDataFrame(issues_event_df.rdd, schema=event_schema_with_action)

member_event_df = member_event_df.select("event_id","type", "actor_id", "org_id","repo_id","public", "created_at", col("payload.action").alias("action"))
# member_event_df = spark.createDataFrame(member_event_df.rdd, schema=event_schema_with_action)

public_event_df = public_event_df.select("event_id","type", "actor_id", "org_id","repo_id","public", "created_at")
# public_event_df = spark.createDataFrame(public_event_df.rdd, schema=event_schema_basic)

release_event_df = release_event_df.select("event_id","type", "actor_id", "org_id","repo_id","public", "created_at", col("payload.action").alias("action"))
# release_event_df = spark.createDataFrame(release_event_df.rdd, schema=event_schema_with_action)

watch_event_df = watch_event_df.select("event_id","type", "actor_id", "org_id","repo_id","public", "created_at", col("payload.action").alias("action"))
# watch_event_df = spark.createDataFrame(watch_event_df.rdd, schema=event_schema_with_action)
import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import { NestedStack, NestedStackProps } from "aws-cdk-lib";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as iam from "aws-cdk-lib/aws-iam";
import * as path from "path";
import * as dotenv from "dotenv";
dotenv.config();

export interface LambdaStackProps extends NestedStackProps {
  // custom interface goes here
}

const python3_12_runtime = new lambda.Runtime(
  "python3.12",
  lambda.RuntimeFamily.PYTHON
);

export class LambdaStack extends NestedStack {
  constructor(scope: Construct, id: string, props: LambdaStackProps) {
    super(scope, id, props);
    // Access to the MainStack
    const mainStack = cdk.Stack.of(this);

    // getMediasLambdaRole Execution Roles:
    const getMediasLambdaRole = new iam.Role(this, "getMediasLambdaRole", {
      assumedBy: new iam.ServicePrincipal("lambda.amazonaws.com"),
    });
    // AWS managed basic lambda execution role
    getMediasLambdaRole.addManagedPolicy(
      iam.ManagedPolicy.fromAwsManagedPolicyName(
        "service-role/AWSLambdaBasicExecutionRole"
      )
    );
    // Custom inline policy for specific needs
    getMediasLambdaRole.addToPolicy(
      new iam.PolicyStatement({
        actions: ["s3:Scan", "s3:GetItem"],
        resources: [
          `arn:aws:dynamodb:${process.env.DEFAULT_AWS_REGION}:${this.account}:table/${process.env.METADATA_TABLE_NAME}`,
        ],
      })
    );

    // Lambda Layers
    const pythonLayer = new lambda.LayerVersion(this, "PythonLayer", {
      code: lambda.Code.fromAsset(
        path.join(__dirname, "../lambdas/python/layer/layer_package.zip")
      ),
      compatibleRuntimes: [python3_12_runtime],
      description: "Lambda Layer for MyFunction",
      layerVersionName: "Choiflix-Python-Layer",
    });

    cdk.Tags.of(pythonLayer).add(mainStack.stackName, "PythonLayer");

    new cdk.CfnOutput(this, "LayerVersionArn", {
      value: pythonLayer.layerVersionArn,
    });

    // Lambda Functions
    const getMedias = new lambda.Function(this, "get_medias", {
      runtime: python3_12_runtime,
      handler: "main.handler",
      code: lambda.Code.fromAsset(
        path.join(__dirname, "../lambdas/python/function/get_medias")
      ),
      environment: {
        METADATA_DDB_TABLE_NAME: process.env.METADATA_DDB_TABLE_NAME || "",
        LOG_LEVEL: process.env.LOG_LEVEL || "",
      },
      layers: [pythonLayer],
      timeout: cdk.Duration.seconds(15),
    });

    cdk.Tags.of(getMedias).add(mainStack.stackName, "get_medias");

    new cdk.CfnOutput(this, "getMediasARN", {
      value: getMedias.functionArn,
    });

    const getMediaUrl = new lambda.Function(this, "get_media_url", {
      runtime: python3_12_runtime,
      handler: "main.handler",
      code: lambda.Code.fromAsset(
        path.join(__dirname, "../lambdas/python/function/get_media_url")
      ),
      environment: {
        CF_PRIVATE_KEY_SECRET_ID: process.env.CF_PRIVATE_KEY_SECRET_ID || "",
        CF_PUBLIC_KEY_ID: process.env.CF_PUBLIC_KEY_ID || "",
        CF_DEFAULT_URL_EXP: process.env.CF_DEFAULT_URL_EXP || "",
        LOG_LEVEL: process.env.LOG_LEVEL || "",
        CLOUDFRONT_DOMAIN: process.env.CLOUDFRONT_DOMAIN || "",
        METADATA_DDB_TABLE_NAME: process.env.METADATA_DDB_TABLE_NAME || "",
      },
      layers: [pythonLayer],
      timeout: cdk.Duration.seconds(15),
    });

    cdk.Tags.of(getMediaUrl).add(mainStack.stackName, "get_media_url");

    new cdk.CfnOutput(this, "getMediaUrlARN", {
      value: getMediaUrl.functionArn,
    });
  }
}

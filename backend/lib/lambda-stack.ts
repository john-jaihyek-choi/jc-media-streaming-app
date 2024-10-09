import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import { NestedStack, NestedStackProps } from "aws-cdk-lib";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as path from "path";

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

    // Lambda Layers
    const pythonLayer = new lambda.LayerVersion(this, "PythonLayer", {
      code: lambda.Code.fromAsset(
        path.join(__dirname, "../lambdas/python/layer")
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
    const functionName1 = new lambda.Function(this, "FunctionName1", {
      runtime: python3_12_runtime,
      handler: "main.main",
      code: lambda.Code.fromAsset(
        path.join(__dirname, "../lambdas/python/function/get_medias")
      ),
      layers: [pythonLayer],
    });

    cdk.Tags.of(functionName1).add(mainStack.stackName, "FunctionName1");

    new cdk.CfnOutput(this, "FunctionArn", {
      value: functionName1.functionArn,
    });
  }
}

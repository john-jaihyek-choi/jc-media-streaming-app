import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import { LambdaStack, LambdaStackProps } from "./lambda-stack";

export class MainStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const lambdaStackProps: LambdaStackProps = {
      // custom LambdaStackProps defined here
    };

    new LambdaStack(this, "LambdaStack", lambdaStackProps);
  }
}

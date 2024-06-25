from agent import ValueIteration, PolicyIteration
import json



def main() -> None:
    value_agent = ValueIteration()
    value_agent.value_iteration()

    value_policy = {}
    for x in value_agent.policy:
        value_policy[str(x)] = value_agent.policy[x]

    with open("policies/valueIteration.json", 'w') as json_value_file:
        json.dump(value_policy, json_value_file)

    policy_agent = PolicyIteration()
    policy_agent.policy_iteration()

    policy_policy = {}
    for y in policy_agent.policy:
        policy_policy[str(y)] = policy_agent.policy[y]
    
    with open("policies/policyIteration.json", 'w') as json_policy_file:
        json.dump(value_policy, json_policy_file)


if __name__ == "__main__":
    main()
